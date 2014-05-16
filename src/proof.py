#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function

__author__ = 'p1002650'
__date__ = '23-04-2014'

from collections import defaultdict

from cases import neighbors_cases
from gather import *
from robot import *

def gen_surrounding(pos, m, n, case, is_single):
    if m <= 0 or n <= 0:
        return

    nb_left = n-3
    if is_single:
        nb_left -= pos

    nb_right = (m-1)*n + pos

    case_btm_row_mask = ( case       & 7) << nb_right
    case_mid_row_mask = ((case >> 3) & 7) << nb_right +   n
    case_top_row_mask = ((case >> 6) & 7) << nb_right + 2*n

    left_shift = nb_right + 3

    for left in xrange(1 << nb_left):

        left_mask = left << left_shift
        for right_mask in xrange(1 << nb_right):

            x = right_mask | case_btm_row_mask | left_mask | case_mid_row_mask

            if is_connex(x, bin(x).count('1'), n):
                yield x

LEFT, MID, RIGHT = 1, 2, 3

def extract_matrix(x, M, N, m, n, i, j):
    """ Extract from x (size M*N) the submatrix located at (i,j) (size m*n)
    """
    # good luck understanding this mess
    b_r_i, b_r_j = i+m-1, j+n-1
    b_r_o = (M - b_r_i -1)*N + (N - b_r_j -1)
    m_o = j + (N - b_r_j -1)
    all1 = (1 << M*N) -1
    res = x >> b_r_o
    for row in xrange(1,m):
        no = (~ ((1 << n*row + m_o) -1)) & all1
        yes = (1 << n*row) -1
        a = (no & res) >> m_o
        b = (yes & res) | a
        res = a | b
    return res & ((1 << m*n) -1)

def unfmt(x):
    r = ['"']
    r.append('1 ' if x & (1 << 8) else '0 ')
    r.append('1 ' if x & (1 << 7) else '0 ')
    r.append('1'  if x & (1 << 6) else '0' )
    r.append('\\n')
    r.append('1 ' if x & (1 << 5) else '0 ')
    r.append('1 ' if x & (1 << 4) else '0 ')
    r.append('1'  if x & (1 << 3) else '0' )
    r.append('\\n')
    r.append('1 ' if x & (1 << 2) else '0 ')
    r.append('1 ' if x & (1 << 1) else '0 ')
    r.append('1'  if x & (1 << 0) else '0' )
    r.append('"')
    return ''.join(r)

def case_of(x, i, j):
    return extract_matrix(x,5,7,3,3,i-1,j-1)

def print_tex(x, m, n):
    robots = []
    for i in xrange(m*n):
        if x & (1 << i) != 0:
            robots.append(str(((n - (i%n) -1), (i/n))))
    print('\\spacee {', (n,m), '} {{', ','.join(robots), '}}', sep='')


single_mask   = cases.fmt('1 1 1' \
                          '1 0 1' \
                          '0 0 0')
leftmost_mask = cases.fmt('1 1 1' \
                          '1 0 0' \
                          '0 0 0')
single_cases   = filter(lambda x: x&  single_mask == 0, neighbors_cases.keys())
leftmost_cases = filter(lambda x: x&leftmost_mask == 0, neighbors_cases.keys())

if __name__ == '__main__':

    m, n = 5, 7

    Robot.space = Space()

    bad_cases = []
    for case in leftmost_cases:
        cpt, bad = 0, 0
        for pos in [LEFT, MID, RIGHT]:
            g = gen_surrounding(pos, m-2, n, case, True)
            next_cases = set()
            for x in g:
                Robot.space.clear()
                Robot.space.add_robots_from_test_case(x, m, n, 0, 0)
                Robot.space.next_step(fast='True')
                rs = Robot.space.get_robots()
                if len(rs) > 2 and (1,3) in rs:
                    y = Robot.space.get_robots_bin(n, m)
                    next_cases.add(case_of(y,1,3))
                    # if case_of(y,1,3) == leftmost_cases[1]:
                    #     bad_cases.append((case,[x]))
                    #     break
                    # next_cases.add(x)
                    # bad += 1
                cpt += 1
            bad_cases.append((case, next_cases))
            print(bad, 'over', cpt)

    Robot.space.clear()

    # dot
    labelized = set()
    print('digraph g {')
    for x, next_step in bad_cases:
        if x not in labelized:
            print(x, ' [label=', unfmt(x), ']', sep='')
            labelized.add(x)
        for y in next_step:
            if y not in labelized:
                print(y, ' [label=', unfmt(y), ']', sep='')
                labelized.add(y)
            print(x, ' -> ', y, ';', sep='')
    print('}')

#     # latex
#     for x, next_steps in bad_cases:
#         print_tex(x, 3, 3)
#         print('\\\\\n')
#         for y in next_steps:
#             print_tex(y, 5, 7)
#         if next_steps:
#             print('\\\\\n')

