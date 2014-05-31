#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function

__author__ = 'Eloi Perdereau'
__date__ = '31-03-2014'

import cases

class Robot(tuple):

    space = None
    arrows = None

    def __init__(self, b):
        super(Robot, self).__init__(tuple(b))
        self.last_surrounding = None
        self.last_pos = None
        self.in_danger = False
        self.done = False

    def get_surroundings(self):
        return Robot.space.get_surroundings(*self)

    def check_if_done(self, surrounding):
        # no neighbors, or in an end_case
        return surrounding == 16 or \
               surrounding == cases.end_cases.get(self.last_surrounding, -1)

    def save_from_danger(self):
        # if we have been disconnected, move to last_pos
        if self.in_danger and \
           self.get_surroundings() & cases.discnx[self.last_surrounding] == 0:
            return self.last_pos
        return self

    def next_position(self):
        if self.done:
            return self

        surrounding = self.get_surroundings()

        if self.is_bad_quincunx_case():
            self.in_danger = cases.symetrics.get(surrounding,-1) in \
                                                            cases.danger_cases
            self.last_pos = self
            self.last_surrounding = surrounding
            return self

#         # check for quincunxness, maybe we must not move this time
#         if cases.quincunx_cases.get(self.last_surrounding, -1) == surrounding:
#             self.last_pos = self
#             self.last_surrounding = surrounding
#             return self

        # compute the next position of the robot
        i, j = self
        di, dj = cases.neighbors_cases.get(surrounding, (0,0))
        r = Robot([i+di, j+dj])
        if r != self:
            Robot.arrows.add('{' + str(self) + '/' + str(r) + '}')

        # check for danger cases (where we may get disconnected)
        r.in_danger = cases.symetrics.get(surrounding,-1) in cases.danger_cases

        # set memory for the next robot and return
        r.last_pos = self
        r.last_surrounding = surrounding
        return r

    def is_bad_quincunx_case(self):
        bad = False
        surrounding = self.get_surroundings()
        if surrounding in cases.quincunx_check:
            (nbhs_to_check, (di, dj)) = cases.quincunx_check[surrounding]
            i, j = self
            shifted_robot = (i+di, j+dj)
            s = Robot.space.get_surroundings(*shifted_robot)
            r = nbhs_to_check & s
            # r is not 0 and a power of 2 if there is only 1 nbh checked
            bad = r != 0 and (r & (r-1)) == 0
        return bad
