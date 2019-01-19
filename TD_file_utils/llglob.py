#!/usr/bin/env python3

"""
Utility to print files/dirs matching pattern.
If found more than 20 elements show only first 10 and last 10.
To show all elements use `-a` option.
Sample of call:
    python llglob.py test/plot_axis_*
    python llglob.py test/plot_axis_* -a
"""

__author__ = 'Boris Polyanskiy'

from argparse import ArgumentParser
import glob
import itertools


def ll_glob(glb, show_all=False):
    """Print all files/folders matching pattern.

    :param glb: pattern (glob).
    :param show_all:
    :return: None
    """

    count = sum(1 for _ in glob.iglob(glb))

    if not show_all and count >= 21:
        c = itertools.count(0)
        for elem in itertools.takewhile(lambda _: next(c) < 10, glob.iglob(glb)):
            print(elem)
        print('... {} more element{}'.format(count - 20, 's' if count > 21 else ''))
        c = itertools.count(0)
        for elem in itertools.dropwhile(lambda _: next(c) + 10 < count, glob.iglob(glb)):
            print(elem)
    else:
        for elem in glob.iglob(glb):
            print(elem)
    print('Total elements found: {}'.format(count))


def main():
    parser = ArgumentParser()
    parser.add_argument('glob')
    parser.add_argument('-a', '--all', action='store_true', help='If selected show all found elements')
    args = parser.parse_args()

    ll_glob(args.glob, show_all=args.all)


if __name__ == '__main__':
    main()
