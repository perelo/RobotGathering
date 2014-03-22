#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '11-03-2014'

import Tkinter as Tk
from random import shuffle
from math import log

import cases

class SpaceView(Tk.Canvas):

    def __init__(self, master, space, width, height, cell_size=10):
        Tk.Canvas.__init__(self, master,
                                 width=width*cell_size,
                                 height=height*cell_size, bd=0)

        self.space = space
        self.cell_size = cell_size
        self.width = width
        self.height = height

        # draw the grid lines
        for i in range(1, width+1):
            self.create_line(i*cell_size, 0,
                             i*cell_size, height*cell_size, fill="grey")
        for i in range(1, height+1):
            self.create_line(0,               i*cell_size,
                             width*cell_size, i*cell_size, fill="grey")
        self.update()

    def update(self):
        # delete all robots present in the grid
        for r in self.find_withtag("robot"):
            self.delete(r)
        # get the bitfield representing the space
        field = self.space.get_robots_bin(self.width, self.height)
        sz = self.width * self.height
        s = self.cell_size
        for i in xrange(sz):
            # convert binary coordinate to x, y coordinates
            y, x = i//self.width, i%self.width
            if field & (1 << sz-i):
                # draw the robot
                r = self.create_oval( x   *s,  y   *s,
                                     (x+1)*s, (y+1)*s, fill="black")
                # attach a tag, so we can get them easily w/ find_withtag()
                self.addtag_withtag("robot", r)

    def next_step(self):
        self.space.next_step()
        self.update()

    def prev_step(self):
        self.space.prev_step()
        self.update()


class Space(object):

    def __init__(self):
        self.step_robots = [set()]   # list of sets of robots (history)
        self.step_index = 0
        self.quescient_step_index = float('inf')

    def get_robots(self):
        return self.step_robots[self.step_index]

    def get_robots_bin(self, w, h):
        # convert i, j coordinates to binary coordinate,
        # at the end, the space will be represented by a bitfield.
        # for now it's not, but the SpaceView update itself w/ a bitfield
        res = 0
        for i, j in self.step_robots[self.step_index]:
            res |= 1 << (w * (h-i-1)) + (w-j-1)
        return res

    def next_step(self):
        # check if we have reached a quescient state
        if self.step_index >= self.quescient_step_index:
            return

        # check, maybe we have already computed the next step
        if self.step_index +1 < len(self.step_robots):
            self.step_index += 1
            return

        # compute all robots movement before actually moving them. Store them
        # either in robots_in_danger or robots_safe, the next step will be an
        # union and the "backup state" will depend on robots_in_dangers
        robots_in_danger = []
        robots_memory = []
        robots_safe = set()
        for r in self.step_robots[self.step_index]:
            r_next, in_danger = self.robot_movement(*r)
            if in_danger:
                # r_next will potentially have to move back to its old pos (r)
                robots_in_danger.append(r_next)
                # memorize the previous surrounding and position
                robots_memory.append((self.get_surroundings(*r), r))
            else:
                # r_next is safe
                robots_safe.add(r_next)
        # "apply" the movement to all the robots, ie create a new "step" in
        # self.step_robots containing all the new robots positions
        next_robots = robots_safe.union(set(robots_in_danger))
        self.step_robots.append(next_robots)
        self.step_index += 1

        # handle robots_in_danger if any
        # (we needed to actually move the robots (i.e the two lines above)
        # before handling robots in danger because of the surroundings)
        if robots_in_danger:
            # for each robots in danger, check if they have reached a
            # non-connex state <=> they have only one neighbor <=>
            # they are in the case 1 or 2
            for i, r_danger in enumerate(robots_in_danger):
                surrounding = self.get_surroundings(*r_danger)
                # let's save the robot in danger :
                # move back if it was disconnexed, ie if none of the neighbors
                # designated by discnx are present (see cases.py)
                prev_surrounding, prev_pos = robots_memory[i]
                r_saved = prev_pos \
                        if surrounding & cases.discnx[prev_surrounding] == 0 \
                        else r_danger
                # add the saved robot
                robots_safe.add(r_saved)
            # update the current robot set to the saved ones
            self.step_robots[self.step_index] = robots_safe

        # if the new state is the same as the previous one, we have are done
        # TODO refactor this : it must be the robots individually who decides
        # wether they are done or not (if, after moving on a case 1,2 or 10,
        # we are in a symetric case, (or if we are alone) then we stop)
        if self.step_robots[self.step_index] == \
                                        self.step_robots[self.step_index-1]:
            self.quescient_step_index = self.step_index-1
            self.step_index -= 1
            self.step_robots.pop()

    def prev_step(self):
        if self.step_index > 0:
            self.step_index -= 1

    def robot_movement(self, i, j):
        # get the surrounding area of the robot i,j
        surrounding = self.get_surroundings(i, j)
        # not ok if it is in a dangerous case
        danger = cases.symetrics.get(surrounding, -1) in (7, 8)
        # get the movement and return
        di, dj = cases.neighbors_cases.get(surrounding, (0,0))
        return (i+di, j+dj), danger

    def get_surroundings(self, i, j, r=1):
        # TODO make it generic using r as the range
        neighboring_cells = (
                (i-1,j-1), (i-1,j  ), (i-1,j+1),
                (i  ,j-1), (i  ,j  ), (i  ,j+1),
                (i+1,j-1), (i+1,j  ), (i+1,j+1),
                )
        res = 0
        n = len(neighboring_cells)
        for k in range(n):
            if neighboring_cells[k] in self.get_robots():
                res |= 1 << (n-k-1)
        return res

    def add_robots_from_test_case(self, t, nb_li, nb_col, di, dj):
        """ Add the robots according to the test_case and the offset
            t : the test_case (int)
            nb_li, nb_col : the dimension of the test_case
            di, dj : the offset
        """
        for i in range(nb_li*nb_col):
            if t & (1 << i):
                self.step_robots[self.step_index]. \
                        add((nb_li-(i//nb_col)+di, nb_col-(i%nb_col)+dj))

def generate_random_connex_space(height, width, n):
    # bitfield of w*h 1s
    s = (1 << (width*height)) -1
    # shuffle all positions
    rpos = range(width*height)
    shuffle(rpos)

    sz = width*height
    for pos in rpos:
        # turn off the bit
        s = s & ~(1 << pos)
        if not is_connex(s, sz-1, width):
            # turn it back on
            s = s | (1 << pos)
        else:
            sz -= 1
            if sz <= n:
                return s
    return s

def is_connex(s, sz, width):
    # TODO : minimize recursion because stack overflow when sz >= 30
    count = [0]     # the count variable, it's array cuz of scoping
    def dfs(x, pos):
        # TODO : memoization ? computation of already called pos is quick
        # check if the bit is set
        if pos < 0 or x & (1 << pos) == 0:
            return x
        # unset the bit and increment counter
        x = x & ~(1 << pos)
        count[0] += 1
        if pos%width != 0:          # not on the right border
            # call on right neighbors
            x = dfs(x, pos+width-1)
            x = dfs(x, pos-1      )
            x = dfs(x, pos-width-1)
        if pos%width != width-1:    # not on the left border
            # call on left neighbors
            x = dfs(x, pos+width+1)
            x = dfs(x, pos+1      )
            x = dfs(x, pos-width+1)
        # call on up and down neighbor
        x = dfs(x, pos+width)
        x = dfs(x, pos-width)
        return x

    # start dfs with the rightmost set bit
    rmost_bit = s & (-s)
    dfs(s, int(log(rmost_bit, 2)))
    return sz == count[0]

if __name__ == '__main__':
    s = Space()

    # the test_cases to be added to the Space
    displayed_test_cases = [

        ( cases.test_cases['square3'],     0,  0 ),
        ( cases.test_cases['square4'],     0,  5 ),
        ( cases.test_cases['square5'],     0, 11 ),
        ( cases.test_cases['square6'],     0, 18 ),
        ( cases.test_cases['square7'],     0, 26 ),
        ( cases.test_cases['square8'],     0, 35 ),
        ( cases.test_cases['stair3'],      10,  0 ),
        ( cases.test_cases['stair4'],      10, 10 ),
        ( cases.test_cases['stair5'],      10, 20 ),
        ( cases.test_cases['stair5,7'],    10, 35 ),
        ( cases.test_cases['bloc2,3'],    21,  0 ),
        ( cases.test_cases['bloc2,4'],    21,  5 ),
        ( cases.test_cases['bloc2,5'],    21, 11 ),
        ( cases.test_cases['bloc3,3'],    21, 18 ),
        ( cases.test_cases['bloc4,4'],    21, 23 ),
        ( cases.test_cases['garden3,7'],  27,  0 ),
        ( cases.test_cases['garden3,9'],  27, 10 ),
        ( cases.test_cases['garden5,9'],  27, 22 ),
        ( cases.test_cases['garden5,11'], 27, 34 ),
        ( cases.test_cases['diag5,6'], 40,  0 ),
        ( cases.test_cases['diag7,8'], 40, 10 ),
        ( cases.test_cases['wierd1'],  40, 20 ),

        ]

    # add the test_cases to the Space
    for dtc in displayed_test_cases:
        test, i, j = dtc
        t, li, col = test
        s.add_robots_from_test_case(t, li, col, i, j)

    # create the window, the canvas and the buttons
    fenetre = Tk.Tk()
    v = SpaceView(fenetre, s, 50, 50)
    btn_next = Tk.Button(fenetre, text='next', command=lambda:v.next_step())
    btn_prev = Tk.Button(fenetre, text='prev', command=lambda:v.prev_step())

    # pack everything and display
    v.pack()
    btn_next.pack()
    btn_prev.pack()
    fenetre.mainloop()
