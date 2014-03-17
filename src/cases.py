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
    rx = (x & (1 << 7)) >> 2 | \
         (x & (1 << 6)) >> 3 | \
         (x & (1 << 5)) >> 5 | \
         (x & (1 << 4)) << 2 | \
         (x & (1 << 3)) >> 2 | \
         (x & (1 << 2)) << 5 | \
         (x & (1 << 1)) << 3 | \
         (x & (1 << 0)) << 2
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)+2)%len(_mvts)]
    return (rx, rmvt)

def _rotate180(case):
    x, mvt = case
    # rotate x
    rx = (x & (1 << 7)) >> 7 | \
         (x & (1 << 6)) >> 5 | \
         (x & (1 << 5)) >> 3 | \
         (x & (1 << 4)) >> 1 | \
         (x & (1 << 3)) << 1 | \
         (x & (1 << 2)) << 3 | \
         (x & (1 << 1)) << 5 | \
         (x & (1 << 0)) << 7
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)+4)%len(_mvts)]
    return (rx, rmvt)

def _rotate270(case):
    x, mvt = case
    # rotate x
    rx = (x & (1 << 7)) >> 5 | \
         (x & (1 << 6)) >> 2 | \
         (x & (1 << 5)) << 2 | \
         (x & (1 << 4)) >> 3 | \
         (x & (1 << 3)) << 3 | \
         (x & (1 << 2)) >> 2 | \
         (x & (1 << 1)) << 2 | \
         (x & (1 << 0)) << 5
    # rotate the mvt
    rmvt = _mvts[(_mvts.index(mvt)-2)%len(_mvts)]
    return (rx, rmvt)

def load_mvt_cases(fname):
    """ Read the file containing all the movement cases,
        than we generate all symetric cases by rotating each one of them
        /!\ this code is terrible, but nevermind
    """
    nosym_cases = {}
    def add_case(b):
        if b:
            coords = b.pop().split(',')
            nosym_cases[fmt(''.join(b))] = tuple(map(int, coords))
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

    # create synonyms
    neighbors_cases = {}
    for case in nosym_cases.iteritems():
        for rotate in [_rotate0, _rotate90, _rotate180, _rotate270]:
            x, mvt = rotate(case)
            neighbors_cases[x] = mvt
    return neighbors_cases


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
neighbors_cases = load_mvt_cases('../res/cases.txt')
