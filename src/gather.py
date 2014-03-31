#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '11-03-2014'

import Tkinter as Tk
from random import shuffle
from math import log
import operator

import cases
from robot import Robot

class SpaceView(Tk.Canvas):

    def __init__(self, master, space, width, height, cell_size=15):
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
            if field & (1 << sz-i-1):
                # draw the robot
                color = "red" if self.space.is_robot_finish(y,x) else "black"
                r = self.create_oval( x   *s,  y   *s,
                                     (x+1)*s, (y+1)*s, fill=color)
                # attach a tag, so we can get them easily w/ find_withtag()
                self.addtag_withtag("robot", r)

    def remove_robot_at(self, x, y):
        r = Robot([y//self.cell_size, x//self.cell_size])
        robots = self.space.get_robots()
        for r2 in robots:
            if r == r2:
                robots.remove(r)
                break

    def add_robot_at(self, x, y):
        r = Robot([y//self.cell_size, x//self.cell_size])
        self.space.get_robots().add(r)

    def next_step(self):
        self.space.next_step()
        self.update()

    def prev_step(self):
        self.space.prev_step()
        self.update()

    def clear(self):
        self.space.clear()
        self.update()


class Space(object):

    def __init__(self):
        self.step_robots = [set()]      # list of sets of robots (history)
        self.robots_finish = dict()     # True if finish, False otherwise
        self.step_index = 0
        self.quescient_step_index = float('inf')
        self.robots_quincunx = set()

    def clear(self):
        self.step_robots = [set()]      # list of sets of robots (history)
        self.robots_finish = dict()     # True if finish, False otherwise
        self.step_index = 0
        self.quescient_step_index = float('inf')
        self.robots_quincunx = set()

    def is_quescient(self):
        return self.quescient_step_index == self.step_index

    def is_robot_finish(self, i, j):
        return self.robots_finish.get(((i,j), self.step_index), False)

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

        # compute all robot's next_positions
        next_robots = []
        for r in self.step_robots[self.step_index]:
            r_next = r.next_position(self.get_surroundings(*r))
            next_robots.append(r_next)

        # do the step, ie move all robots in the space
        self.step_robots.append(set(next_robots))
        self.step_index += 1

        # some robots may be in danger, do another round to save them
        robots_safe = set()
        for r in next_robots:
            r_next = r.save_from_danger(self.get_surroundings(*r))
            robots_safe.add(r_next)
        self.step_robots[self.step_index] = robots_safe

        # some robots may have done, note and count them
        nb_done_robots = 0
        for r in self.step_robots[self.step_index]:
            if r.check_if_done(self.get_surroundings(*r)):
                nb_done_robots += 1
                self.robots_finish[(r, self.step_index)] = True

        # maybe we are globally quescient
        if nb_done_robots >= len(self.step_robots[self.step_index]):
            self.quescient_step_index = self.step_index

    def prev_step(self):
        if self.step_index > 0:
            self.step_index -= 1

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
                        add(Robot([nb_li-(i//nb_col)+di-1,
                                   nb_col-(i%nb_col)+dj-1]))

def generate_random_connex_space(height, width, n):
    # bitfield of w*h 1s
    s = (1 << (width*height)) -1
    # shuffle all positions
    rpos = range(width*height)
    shuffle(rpos)

    count = width*height
    print 'n =', n
    while count > n and rpos:
        pos = rpos.pop()
        # turn off the bit
        s = s & ~(1 << pos)
        count -= 1
        # print pos, count, bin(s)
        if not is_connex(s, count, width):
            # turn it back on
            s = s | (1 << pos)
            count += 1
            rpos.insert(0, pos)
    return s

def is_connex(s, sz, width):
    count = 0
    # start with the rightmost bit
    rmost_bit = s & (-s)
    queue = [int(log(rmost_bit, 2))]
    while queue:   # while queue is not empty
        pos = queue.pop()
        if pos >= 0 and s & (1 << pos) != 0:    # if s has a robot at pos
            # unset the bit and increment counter
            s = s & ~(1 << pos)
            count += 1
            # add it's neighbors in the queue and continue
            if pos%width != 0:          # not on the right border
                # add right neighbors
                queue.append(pos+width-1)
                queue.append(pos-1      )
                queue.append(pos-width-1)
            if pos%width != width-1:    # not on the left border
                # add left neighbors
                queue.append(pos+width+1)
                queue.append(pos+1      )
                queue.append(pos-width+1)
            # add up and down neighbors
            queue.append(pos+width)
            queue.append(pos-width)
    return count == sz

def fill_with_test_cases(s):
    # the test_cases to be added to the Space
    displayed_test_cases = [

        ( cases.test_cases['square3'],      0,  0  ),
        ( cases.test_cases['square4'],      0,  5  ),
        ( cases.test_cases['square5'],      0,  11 ),
        ( cases.test_cases['square6'],      0,  18 ),
        ( cases.test_cases['square7'],      0,  26 ),
        ( cases.test_cases['square8'],      0,  35 ),
        ( cases.test_cases['stair3'],       10, 0  ),
        ( cases.test_cases['stair4'],       10, 10 ),
        ( cases.test_cases['stair5'],       10, 20 ),
        ( cases.test_cases['stair5,7'],     10, 35 ),
        ( cases.test_cases['bloc2,3'],      21, 0  ),
        ( cases.test_cases['bloc2,4'],      21, 5  ),
        ( cases.test_cases['bloc2,5'],      21, 11 ),
        ( cases.test_cases['bloc3,3'],      21, 18 ),
        ( cases.test_cases['bloc4,4'],      21, 23 ),
        ( cases.test_cases['garden3,7'],    27, 0  ),
        ( cases.test_cases['garden3,9'],    27, 10 ),
        ( cases.test_cases['garden5,9'],    27, 22 ),
        ( cases.test_cases['garden5,11'],   27, 34 ),
        ( cases.test_cases['diag5,6'],      40, 0  ),
        ( cases.test_cases['diag7,8'],      40, 10 ),
        ( cases.test_cases['wierd1'],       40, 20 ),
        ( cases.test_cases['circle1'],      0,  50 ),
        ( cases.test_cases['circle2'],      20, 50 ),
        ( cases.test_cases['spiky-square'], 40, 50 ),

        ]

    # add the test_cases to the Space
    for dtc in displayed_test_cases:
        test, i, j = dtc
        t, li, col = test
        s.add_robots_from_test_case(t, li, col, i, j)


def fill_with_random_connex(s):
    li, col = 30, 30
    r = generate_random_connex_space(li, col, (li*col)/4)
    s.add_robots_from_test_case(r, li, col, 10, 10)

def remove_robot(view):
    def fct(event):
        view.remove_robot_at(event.x, event.y)
        view.update()
    return fct

def add_robot(view):
    def fct(event):
        view.add_robot_at(event.x, event.y)
        view.update()
    return fct

if __name__ == '__main__':
    s = Space()

    # fill_with_random_connex(s)
    fill_with_test_cases(s)

    # create the window, the canvas and the buttons
    fenetre = Tk.Tk()
    v = SpaceView(fenetre, s, 70, 50)
    btn_next = Tk.Button(fenetre, text='next', command=lambda:v.next_step())
    btn_prev = Tk.Button(fenetre, text='prev', command=lambda:v.prev_step())
    btn_clear = Tk.Button(fenetre, text='clear', command=lambda:v.clear())
    v.bind("<Button-3>", remove_robot(v))
    v.bind("<B3-Motion>", remove_robot(v))
    v.bind("<Button-1>", add_robot(v))
    v.bind("<B1-Motion>", add_robot(v))

    # pack everything and display
    v.pack()
    btn_next.pack()
    btn_prev.pack()
    btn_clear.pack()
    fenetre.mainloop()
