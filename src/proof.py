#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function

__author__ = 'p1002650'
__date__ = '23-04-2014'

from collections import defaultdict

import cases
from gather import *
from robot import *
from leftmost import leftmost_nbh_cases

def gen_surrounding(m, n, presents, not_presents):
    if m <= 0 or n <= 0:
        return
    sz = 1 << (m*n)
    for i in range(1, sz):
        # all '1's in *presents* must be in i
        # none of '1's in *not_presents* must be in i
        # i must be connex
        if i & presents == presents and \
           i & not_presents == 0 and \
           is_connex(i, bin(i).count('1'), n):
            yield i

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

if __name__ == '__main__':

    m, n = 5, 7

    Robot.space = Space()

    bad_cases = []
    for presents, not_presents in leftmost_nbh_cases:
        cpt, bad = 0, 0
        g = gen_surrounding(m-2, n, presents, not_presents)
        next_cases = set()
        for x in g:
            Robot.space.clear()
            Robot.space.add_robots_from_test_case(x, m, n, 0, 0)
            Robot.space.next_step()
            y = Robot.space.get_robots_bin(n, m)
            rs = Robot.space.get_robots()
            if len(rs) <= 2:
                continue
            for undesirable_robot in [ (2,4),(2,2),(2,3) ]:
                a, b = undesirable_robot
                if undesirable_robot in rs :#and \
       # case_of(y,*undesirable_robot) == case_of(leftmost_nbh_cases[0][0],2,3):
                    next_cases.add(case_of(y,*undesirable_robot))
                    # next_cases.add(x)
            # if y & next_step_presents != next_step_presents or \
            #    y & next_step_not_presents != 0:
            #     bad_cases.append(x)
            #     bad += 1
            cpt += 1
        cur_case = extract_matrix(presents, m, n, 3, 3, 1, 2)
        bad_cases.append((cur_case, next_cases))
        # print(bad, 'over', cpt)

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
                print(y, ' [lbl=', unfmt(y), ']', sep='')
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

