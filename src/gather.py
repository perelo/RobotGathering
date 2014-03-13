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
            self.create_line(i*cell_size, 0, i*cell_size, height*cell_size, fill="grey")
        for i in range(1, height+1):
            self.create_line(0, i*cell_size, width*cell_size, i*cell_size, fill="grey")
        self.update()

    def update(self):
        # delete all robots present in the grid
        for r in self.find_withtag("robot"):
            self.delete(r)
        # create all robots in the space
        s = self.cell_size
        for robot in self.space.get_robots():
            j, i = robot
            r = self.create_oval( i   *s,  j   *s,
                                 (i+1)*s, (j+1)*s, fill="black")
            self.addtag_withtag("robot", r)

    def next_step(self):
        self.space.next_step()
        self.update()

class Space(object):

    # TODO maybe refactor everything and use a bitfield to represent the space

    def __init__(self):
        self.robots = []

    def remove_robot(self, i, j):
        self.robots.remove((i,j))

    def add_robot(self, i, j):
        self.robots.append((i,j))

    def get_robots(self):
        return self.robots

    def next_step(self):
        next_robots = set()
        for r in self.robots:
            next_robots.add(self.robot_movement(*r))
        self.robots = list(next_robots)

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
            if neighboring_cells[k] in self.robots:
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
                self.add_robot(nb_li-(i//nb_col)+di, nb_col-(i%nb_col)+dj)


s = Space()

test, li, col = cases.test1
s.add_robots_from_test_case(test, li, col, 22, 22)

fenetre = Tk.Tk()
v = SpaceView(fenetre, s, 50, 50)
btn = Tk.Button(fenetre, text='next step', command=lambda:v.next_step())

v.pack()
btn.pack()
fenetre.mainloop()
