#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Neighbors cases and test cases for the gathering of robots problem
    read from files and create the dict
"""

__author__ = 'Eloi Perdereau'
__date__ = '13-03-2014'

from re import sub

def fmt(s):
    """ Format from string of bits to integer """
    return int(sub(r'\s+', '', s), 2)

_mvts = [
    (-1,-1),
    (-1, 0),
    (-1, 1),
    ( 0, 1),
    ( 1, 1),
    ( 1, 0),
    ( 1,-1),
    ( 0,-1),
]

def _rotate0(case):
    return case

def _rotate90(case):
    x, mvt = case
    # rotate x
    rx = (x & (1 << 8)) >> 2 | \
         (x & (1 << 7)) >> 4 | \
         (x & (1 << 6)) >> 6 | \
         (x & (1 << 5)) << 2 | \
         (x & (1 << 4)) << 0 | \
         (x & (1 << 3)) >> 2 | \
         (x & (1 << 2)) << 6 | \
         (x & (1 << 1)) << 4 | \
         (x & (1 << 0)) << 2
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)+2)%len(_mvts)]
    return (rx, rmvt)

def _rotate180(case):
    x, mvt = case
    # rotate x
    rx = (x & (1 << 8)) >> 8 | \
         (x & (1 << 7)) >> 6 | \
         (x & (1 << 6)) >> 4 | \
         (x & (1 << 5)) >> 2 | \
         (x & (1 << 4)) << 0 | \
         (x & (1 << 3)) << 2 | \
         (x & (1 << 2)) << 4 | \
         (x & (1 << 1)) << 6 | \
         (x & (1 << 0)) << 8
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)+4)%len(_mvts)]
    return (rx, rmvt)

def _rotate270(case):
    x, mvt = case
    # rotate x
    rx = (x & (1 << 8)) >> 6 | \
         (x & (1 << 7)) >> 2 | \
         (x & (1 << 6)) << 2 | \
         (x & (1 << 5)) >> 4 | \
         (x & (1 << 4)) << 0 | \
         (x & (1 << 3)) << 4 | \
         (x & (1 << 2)) >> 2 | \
         (x & (1 << 1)) << 2 | \
         (x & (1 << 0)) << 6
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)-2)%len(_mvts)]
    return (rx, rmvt)

def load_mvt_cases(fname):
    """ Read the file containing all the movement cases,
        than we generate all symetric cases by rotating each one of them
        /!\ this code is terrible, but nevermind
    """
    nosym_cases = []
    def add_case(b):
        if b:
            str_coords = b.pop().split(',')
            coords = tuple(map(int, str_coords))
            x = fmt(''.join(b))
            nosym_cases.append((x, coords))
    with open(fname, 'r') as f:
        b = []
        for l in f:
            if not l.strip():
                add_case(b)
                b = []
            else:
                if not l[0] == '#':
                    b.append(l)
    add_case(b)

    # create symetric cases
    neighbors_cases = {}
    symetrics = {}
    discnx = {}
    i = 1
    for case in nosym_cases:
        for rotate in [_rotate0, _rotate90, _rotate180, _rotate270]:
            x, mvt = rotate(case)
            neighbors_cases[x] = mvt
            symetrics[x] = i
            # add discnx for the special bad cases :
            # they are the neighbors to check after a dangerous move
            # (at least one neighbor must be present)
            if i in danger_cases:
                if i == 7:
                    dx, _ = rotate((fmt('0 0 0' \
                                        '0 0 1' \
                                        '0 1 1'), (1,1)))
                if i == 8:
                    dx, _ = rotate((fmt('0 0 0' \
                                        '1 0 0' \
                                        '1 1 0'), (1,1)))
                if i == 13:
                    dx, _ = rotate((fmt('1 1 0' \
                                        '1 0 0' \
                                        '0 0 0'), (1,1)))
                if i == 14:
                    dx, _ = rotate((fmt('0 1 1' \
                                        '0 0 1' \
                                        '0 0 0'), (1,1)))
                discnx[x] = dx
        i += 1
    return neighbors_cases, symetrics, discnx

danger_cases = (7, 8, 13, 14)

def create_end_cases():
    end_cases_x = ((fmt('1 0 0' \
                        '0 1 0' \
                        '0 0 0'), (1,1)),
                   (fmt('0 1 0' \
                        '0 1 0' \
                        '0 0 0'), (1,1)),
                   (fmt('1 1 0' \
                        '1 1 0' \
                        '0 0 0'), (1,1)),
                  )
    # /!\ Don't look the next paragraph !!! it's terrible, i'm ashamed...
    # anyway, it's completely unreadable, so no one will know how much it sucks
    end_cases = {}
    for x in end_cases_x:
        for rotate in [_rotate0, _rotate90, _rotate180, _rotate270]:
            rx = rotate(x)
            end_cases[rx[0]] = _rotate180(rx)[0]
    return end_cases

def create_quincunx_cases():
    quincunx_cases_x = ((fmt('1 0 1' \
                             '0 1 0' \
                             '0 0 0'), (1,1)),

                        (fmt('0 0 1' \
                             '0 1 0' \
                             '0 0 1'), (1,1)),

                        (fmt('0 0 1' \
                             '1 1 0' \
                             '0 0 0'), (1,1)),

                        (fmt('1 0 0' \
                             '0 1 1' \
                             '0 0 0'), (1,1)),

                        (fmt('0 0 1' \
                             '0 1 0' \
                             '0 1 0'), (1,1)),

                        (fmt('0 1 0' \
                             '0 1 0' \
                             '0 0 1'), (1,1)),
                       )
    quincunx_cases = {}
    for x in quincunx_cases_x:
        rx = _rotate180(x)
        quincunx_cases[x[0]]  = rx[0]
        quincunx_cases[rx[0]] = x[0]
    return quincunx_cases

def load_test_cases(fname):
    """ Read the file containing test cases
        ie portions of space with connected robots inside
        /!\ this code is terrible too, but nevermind
    """
    bs = {}
    with open(fname, 'r') as f:
        def add_case(name, b):
            if b:
                bs[name] = (fmt(''.join(b)), len(b), len(b[0]))
        b = []
        name = ''
        for l in f:
            if not l.strip():
                add_case(name, b)
                b = []
            elif l[0].isalpha():
                name = l.strip()
            else:
                b.append(l.strip().replace(' ',''))
        add_case(name,b)
    return bs

test_cases = load_test_cases('../res/tests.txt')
neighbors_cases, symetrics, discnx = load_mvt_cases('../res/cases.txt')
end_cases = create_end_cases()
quincunx_cases = create_quincunx_cases()
