#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'p1002650'
__date__ = '30-04-2014'

import Tkinter as Tk

from gather import *

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

def display_space(s):
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

if __name__ == '__main__':
    s = Space()
    Robot.space = s

    # test_rectangle_complexity(s)
    # fill_with_random_connex(s, 30, 30, (30*30))
    fill_with_test_cases(s)
    # fill_with_blocs_and_squares(s)

    display_space(s)
