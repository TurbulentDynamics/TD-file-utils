#!/usr/bin/env python3

__author__ = "Nile ÓBroin"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to check if there are any files missing in a sequence of steps.

Args:

  Input:
    Shell glob expression, quoted

  Output:
    Files present: [53-54,56-57...]
    Missing files: [51-52,55,58-60,63-66,69-70,73,76-77,79-81,84-88,90-101,103-124,126-127,129-133]
"""

import os, glob, sys, re
import argparse
import itertools
from collections import defaultdict

def present_as_ranges(lst):
    for _,b in itertools.groupby(enumerate(sorted(lst)), lambda x: x[1]-x[0]):
        b = tuple(b)
        start, end = b[0][1], b[-1][1]
        yield "%d-%d" % (start, end) if start != end else str(start)

def missing_as_ranges(lst):
    lst = [ x for x in range(min(lst), max(lst)) if x not in lst ]
    return present_as_ranges(lst)

def get_steps(glb):
    dir_list = glob.glob(glb)
    steps = defaultdict(list)
    regex = re.compile(r'step_(\d+)')
    for d in dir_list:
        m = regex.search(d)
        if m is not None:
            step = m.group(1)
            idx = d.replace(step, '*')
            steps[idx].append(int(step))
    return steps

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utility to check if there are any files missing in a sequence of steps.')
    parser.add_argument('glob', help='Shell glob expression, quoted')

    args, unknown = parser.parse_known_args()
    steps = get_steps(args.glob)

    for k in steps.keys():
       print("\nBatch «%s»:" % k)
       print("  Files present: [%s]" % ','.join(x for x in present_as_ranges(steps[k])))
       print("  Files missing: [%s]" % ','.join(x for x in missing_as_ranges(steps[k])))
