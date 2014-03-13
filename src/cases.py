#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Neighbors cases and test cases for the gathering of robots problem
"""

__author__ = 'Eloi Perdereau'
__date__ = '13-03-2014'

def fmt(s):
    """ Format from string of bits to integer """
    return int(s.strip().replace(' ',''), 2)

neighbors_cases = {

    # one neighbors
    fmt('1 0 0' \
        '0   0' \
        '0 0 0') : (-1,-1),
    fmt('0 1 0' \
        '0   0' \
        '0 0 0') : (-1, 0),
    fmt('0 0 1' \
        '0   0' \
        '0 0 0') : (-1, 1),
    fmt('0 0 0' \
        '1   0' \
        '0 0 0') : ( 0,-1),
    fmt('0 0 0' \
        '0   1' \
        '0 0 0') : ( 0, 1),
    fmt('0 0 0' \
        '0   0' \
        '1 0 0') : ( 1,-1),
    fmt('0 0 0' \
        '0   0' \
        '0 1 0') : ( 1, 0),
    fmt('0 0 0' \
        '0   0' \
        '0 0 1') : ( 1, 1),

    # two neighbors : themselves neighbors
    fmt('1 1 0' \
        '0   0' \
        '0 0 0') : (-1, 0),
    fmt('0 1 1' \
        '0   0' \
        '0 0 0') : (-1, 0),
    fmt('0 0 1' \
        '0   1' \
        '0 0 0') : ( 0, 1),
    fmt('0 0 0' \
        '0   1' \
        '0 0 1') : ( 0, 1),
    fmt('0 0 0' \
        '0   0' \
        '0 1 1') : ( 1, 0),
    fmt('0 0 0' \
        '0   0' \
        '1 1 0') : ( 1, 0),
    fmt('0 0 0' \
        '1   0' \
        '1 0 0') : ( 0,-1),
    fmt('1 0 0' \
        '1   0' \
        '0 0 0') : ( 0,-1),

    # two neighbors : on non-opposite orthos
    fmt('0 1 0' \
        '1   0' \
        '0 0 0') : (-1,-1),
    fmt('0 1 0' \
        '0   1' \
        '0 0 0') : (-1, 1),
    fmt('0 0 0' \
        '0   1' \
        '0 1 0') : ( 1, 1),
    fmt('0 0 0' \
        '1   0' \
        '0 1 0') : ( 1,-1),

    # two neighbors : on non-opposite corners
    fmt('1 0 1' \
        '0   0' \
        '0 0 0') : (-1, 0),
    fmt('0 0 1' \
        '0   0' \
        '0 0 1') : ( 0, 1),
    fmt('0 0 0' \
        '0   0' \
        '1 0 1') : ( 1, 0),
    fmt('1 0 0' \
        '0   0' \
        '1 0 0') : ( 0,-1),

    # three neighbors : on a line
    fmt('1 1 1' \
        '0   0' \
        '0 0 0') : (-1, 0),
    fmt('0 0 1' \
        '0   1' \
        '0 0 1') : ( 0, 1),
    fmt('0 0 0' \
        '0   0' \
        '1 1 1') : ( 1, 0),
    fmt('1 0 0' \
        '1   0' \
        '1 0 0') : ( 0,-1),

    # four neighbor : doing a 'L'
    fmt('1 1 1' \
        '0   1' \
        '0 0 0') : (-1, 0),
    fmt('1 1 1' \
        '1   0' \
        '0 0 0') : (-1, 0),
    fmt('0 1 1' \
        '0   1' \
        '0 0 1') : ( 0, 1),
    fmt('0 0 1' \
        '0   1' \
        '0 1 1') : ( 0, 1),
    fmt('0 0 0' \
        '1   0' \
        '1 1 1') : ( 1, 0),
    fmt('0 0 0' \
        '0   1' \
        '1 1 1') : ( 1, 0),
    fmt('1 1 0' \
        '1   0' \
        '1 0 0') : ( 0,-1),
    fmt('1 0 0' \
        '1   0' \
        '1 1 0') : ( 0,-1),

}

# test cases

test1 = \
    (fmt('1 1 1' \
         '1 0 1' \
         '1 1 1'), 3, 3)

test2 = \
    (fmt('1 1 1 1' \
         '1 0 0 1' \
         '1 0 0 1' \
         '1 1 1 1'), 4, 4)

test3 = \
    (fmt('1 1 1 1 1' \
         '1 0 0 0 1' \
         '1 0 0 0 1' \
         '1 0 0 0 1' \
         '1 1 1 1 1'), 5, 5)

test4 = \
    (fmt('1 1 1 0 0' \
         '1 0 1 0 0' \
         '1 0 1 1 1' \
         '1 0 0 0 1' \
         '1 1 1 1 1'), 5, 5)

test5 = \
    (fmt('1 1 1 1 1'), 1, 5)

test6 = \
    (fmt('1 1 1 1 1 1 1 1 1 1'), 1, 10)

test7 = \
    (fmt('1 1 1' \
         '1 1 1'), 2, 3)

test8 = \
    (fmt('1 1 1' \
         '1 0 1'), 2, 3)
