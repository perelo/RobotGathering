#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '11-03-2014'

from random import shuffle
from math import log, floor, ceil

from cases import test_cases
from robot import Robot

from collections import deque

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
            r_next = r.next_position()
            next_robots.append(r_next)

        # do the step, ie move all robots in the space
        self.step_robots.append(set(next_robots))
        self.step_index += 1

        # some robots may be in danger, do another round to save them
        robots_safe = set()
        for r in next_robots:
            r_next = r.save_from_danger()
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
    while count > n and rpos:
        pos = rpos.pop()
        # turn off the bit
        s = s & ~(1 << pos)
        count -= 1
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
    queue = deque()
    queue.append(int(log(rmost_bit, 2)))
    while queue:   # while queue is not empty
        pos = queue.pop()
        if pos >= 0 and s & (1 << pos) != 0:    # if s has a robot at pos
            # unset the bit and increment counter
            s = s & ~(1 << pos)
            count += 1
            # add it's neighbors in the queue and continue
            if pos%width != 0:          # not on the right border
                # add right neighbors
                queue.extend((pos+width-1, pos-1, pos-width-1))
            if pos%width != width-1:    # not on the left border
                # add left neighbors
                queue.extend((pos+width+1, pos+1, pos-width+1))
            # add up and down neighbors
            queue.extend((pos+width, pos-width))
    return count == sz

def fill_with_test_cases(s):
    # the test_cases to be added to the Space
    displayed_test_cases = [

        ( test_cases['square3'],      0,  0  ),
        ( test_cases['square4'],      0,  5  ),
        ( test_cases['square5'],      0,  11 ),
        ( test_cases['square6'],      0,  18 ),
        ( test_cases['square7'],      0,  26 ),
        ( test_cases['square8'],      0,  35 ),
        ( test_cases['stair3'],       10, 0  ),
        ( test_cases['stair4'],       10, 10 ),
        ( test_cases['stair5'],       10, 20 ),
        ( test_cases['stair5,7'],     10, 35 ),
        ( test_cases['bloc2,3'],      21, 0  ),
        ( test_cases['bloc2,4'],      21, 5  ),
        ( test_cases['bloc2,5'],      21, 11 ),
        ( test_cases['bloc3,3'],      21, 18 ),
        ( test_cases['bloc4,4'],      21, 23 ),
        ( test_cases['garden3,7'],    27, 0  ),
        ( test_cases['garden3,9'],    27, 10 ),
        ( test_cases['garden5,9'],    27, 22 ),
        ( test_cases['garden5,11'],   27, 34 ),
        ( test_cases['diag5,6'],      40, 0  ),
        ( test_cases['diag7,8'],      40, 10 ),
        ( test_cases['wierd1'],       40, 20 ),
        ( test_cases['circle1'],      0,  50 ),
        ( test_cases['circle2'],      20, 50 ),
        ( test_cases['spiky-square'], 40, 50 ),

        ]

    # add the test_cases to the Space
    for dtc in displayed_test_cases:
        test, i, j = dtc
        t, li, col = test
        s.add_robots_from_test_case(t, li, col, i, j)

def fill_with_blocs_and_squares(s):
    def b(m,n):
        return gen_block(m,n), m, n
    def r(m,n):
        return gen_rect (m,n), m, n
    displayed_test_cases = [
        ( r(10,20),  1,  1 ),
        ( b(10,20), 12,  1 ),
        ( r(10,21),  1, 25 ),
        ( b(10,21), 12, 25 ),
        ( r(11,20), 26,  1 ),
        ( b(11,20), 38,  1 ),
        ( r(11,21), 26, 25 ),
        ( b(11,21), 38, 25 ),
        ( r(16,16),  1, 50 ),
        ( b(16,16), 21, 50 ),
        ]

    # add the test_cases to the Space
    for dtc in displayed_test_cases:
        test, i, j = dtc
        t, li, col = test
        s.add_robots_from_test_case(t, li, col, i, j)


def fill_with_random_connex(s, li, col, n):
    print li, 'x', col, ', n =', n,
    r = generate_random_connex_space(li, col, n)
    s.add_robots_from_test_case(r, li, col, 0, 0)

def gen_block(m, n):
    if m <= 0 or n <= 0:
        return 0
    return (1 << (m*n)) - 1

def gen_rect(m, n):
    if m <= 0 or n <= 0:
        return 0
    top = (1 << n) - 1
    mid = (1 << (n-1)) | 1
    res = (top << ((m-1)*n))    # top row
    res |= top                  # bottom row
    for i in xrange(1,m-1):     # middle rows
        res |= mid << (n*i)
    return res

def test_rectangle_complexity(s):
    for m in xrange(30, 51):
        for n in xrange(30, 51):
            s.clear()
            t = gen_rect(m,n)
            s.add_robots_from_test_case(t, m, n, 0, 0)
            count = 0
            while not s.is_quescient():
                s.next_step()
                count += 1
            print m, n, 'donne', count
            l, L = min(m,n), max(m,n)
            assert count ==   ceil((L-4)/2.0) \
                            + floor(l/2.0)*2 - 2*(1 - l%2) \
                            + (1 - (l%2 and L%2))
