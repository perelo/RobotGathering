#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '31-03-2014'

import cases

class Robot(tuple):

    def __init__(self, b):
        super(Robot, self).__init__(tuple(b))
        self.last_surrounding = None
        self.last_pos = None
        self.in_danger = False
        self.quincunx = False
        self.done = False

    def check_if_done(self, surrounding):
        # no neighbors, or in an end_case
        return surrounding == 16 or \
               surrounding == cases.end_cases.get(self.last_surrounding, -1)

    def save_from_danger(self, surrounding):
        # if we have been disconnected, move to last_pos
        if self.in_danger and \
           surrounding & cases.discnx[self.last_surrounding] == 0:
            return self.last_pos
        return self

    def next_position(self, surrounding):
        if self.done:
            return self

        # check for quincunxness, maybe we must not move this time
        if self.quincunx and \
           cases.quincunx_cases[self.last_surrounding] == surrounding:
            self.quincunx = False
            return self

        # compute the next position of the robot
        i, j = self
        di, dj = cases.neighbors_cases.get(surrounding, (0,0))
        r = Robot([i+di, j+dj])

        # set if robot is in quincunx position
        r.quincunx = surrounding in cases.quincunx_cases

        # check for danger cases (where we may get disconnected)
        r.in_danger = cases.symetrics.get(surrounding,-1) in cases.danger_cases

        # set memory for the next robot and return
        r.last_pos = self
        r.last_surrounding = surrounding
        return r
