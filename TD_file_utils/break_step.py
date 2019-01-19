#!/usr/bin/env python3

"""
Utility to organize dirs/files via glob pattern.
Multiprocessing. To set count of processes use '-n' parameter. Default processes count - count of CPU at host PC.
Override source file structure.
Sample of call:
    python break_step.py test/plot_axis_* step 50 -n 8
"""

__author__ = 'Boris Polyanskiy'

from argparse import ArgumentParser
import glob
import itertools
import re

from TD_file_utils.mvglob import move
from TD_file_utils.stuff import CPU_COUNT, pool

regex = re.compile(r'(.*)_step_(\d+)')


def calculate_interval(check, start, step):
    """Calculate interval of check.

    :param check: interesting value.
    :param start: start value of intervals.
    :param step: step of interval.
    :return: left border of interval.
    """

    for x in itertools.count(start, step):
        if x <= check < x + step:
            return x


def get_element(glb, step):
    """Take pattern (glb) and yield each matched element with folder for move (after calculating interval).

    :param glb: pattern (glob)
    :param step: step of interval (int)
    :return: tuple with path to matched file/folder and folder for move.
    """

    start = None

    for elem in glob.iglob(glb):
        '''
        found = regex.search(elem)
        if not found:
            continue
        name, value = found.groups()
        '''

        # '''
        found = elem.find('_step_')
        if not found:
            continue

        name = elem[:found]
        # faster than regex?
        value = ''.join(itertools.takewhile(str.isdigit, elem[found+6:]))
        # '''
        if start is None:
            start = int(value)
        interval = calculate_interval(int(value), start, step)
        res = '{}_{}_{}'.format(name, interval, interval+step-1)
        start = interval
        yield elem, res


def break_step(glb, step, proc_count):
    """Organize dirs/files via glob pattern.

    :param glb: pattern (glob)
    :param step: step for breaking
    :param proc_count: count of processes.
    :return: None
    """
    pool(move, iter(get_element(glb, step)), proc_count)


def main():
    parser = ArgumentParser(description='Utility to organize dirs/files via glob pattern.')
    parser.add_argument('glob', help='Shell glob expression, quoted')
    parser.add_argument('step', type=int, help='Break interval')
    parser.add_argument('-n', '--numprocs', type=int, help='Process count (default: 8)', default=CPU_COUNT)
    args = parser.parse_args()

    break_step(args.glob, args.step, args.numprocs)


if __name__ == '__main__':
    main()
