#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '11-03-2014'

import Tkinter as Tk
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
        self.step_robots = [[]]   # list of list of robots (history)
        self.step_index = 0

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
        # check, maybe we have already computed it
        if self.step_index +1 >= len(self.step_robots):
            # compute all robots movement before actually moving them
            next_robots = set()
            for r in self.step_robots[self.step_index]:
                next_robots.add(self.robot_movement(*r))
            self.step_robots.append(list(next_robots))
        self.step_index += 1

    def prev_step(self):
        if self.step_index > 0:
            self.step_index -= 1

    def robot_movement(self, i, j):
        di, dj = cases.neighbors_cases.get(self.get_surroundings(i, j), (0,0))
        return (i+di, j+dj)

    def get_surroundings(self, i, j, r=1):
        # TODO make it generic using r as the range
        neighboring_cells = (
                (i-1,j-1), (i-1,j  ), (i-1,j+1),
                (i  ,j-1),            (i  ,j+1),
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
                        append((nb_li-(i//nb_col)+di, nb_col-(i%nb_col)+dj))


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
