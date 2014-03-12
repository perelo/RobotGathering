#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '11-03-2014'

import Tkinter as Tk

class SpaceView(Tk.Canvas):

    def __init__(self, master, space, cell_size=10):
        Tk.Canvas.__init__(self, master,
                                 width=space.width*cell_size,
                                 height=space.height*cell_size, bd=0)

        self.space = space
        self.cell_size = cell_size

        # draw the grid lines
        for i in range(1, space.width+1):
            self.create_line(i*cell_size, 0, i*cell_size, space.height*cell_size, fill="grey")
        for i in range(1, space.height+1):
            self.create_line(0, i*cell_size, space.width*cell_size, i*cell_size, fill="grey")
        self.update()

    def update(self):
        # delete all robots present in the grid
        for r in self.find_withtag("robot"):
            self.delete(r)
        # create all robots in the space
        s = self.cell_size
        for robot in self.space.get_robots():
            i, j = robot
            r = self.create_oval( i   *s,  j   *s,
                                 (i+1)*s, (j+1)*s, fill="black")
            self.addtag_withtag("robot", r)

    def next_step(self):
        self.space.next_step()
        self.update()

class Space(object):

    # TODO maybe refactor everything and use a bitfield to represent the space

    def __init__(self, height, width):
        self.robots = []
        self.height = height
        self.width = width

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
        # TODO here will be the algorithm based on surroundings
        return (i, j+1)

    def get_surroundings(self, i, j, r=1):
        # TODO make it generic using r as the range
        neighboring_cells = (
                (i+1,j-1), (i+1,j  ), (i+1,j+1),
                (i  ,j-1),            (i  ,j+1),
                (i-1,j-1), (i-1,j  ), (i-1,j+1),
                )
        return ( x for x in neighboring_cells if x in self.robots )

s = Space(50, 50)
s.add_robot(0, 0)
s.add_robot(0, 1)
s.add_robot(40, 4)

fenetre = Tk.Tk()
v = SpaceView(fenetre, s)
btn = Tk.Button(fenetre, text='next step', command=lambda:v.next_step())

v.pack()
btn.pack()
fenetre.mainloop()
