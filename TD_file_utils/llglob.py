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


def ll_glob(glb, show_all=False):
    """Print all files/folders matching pattern.

    :param glb: pattern (glob).
    :param show_all:
    :return: None
    """

    glob_list = sorted(glob.glob(glb))
    glob_count = len(glob_list)
    if not show_all and glob_count > 21:
        for elem in glob_list[:10]:
            print(elem)
        print('... {} more element{}'.format(glob_count - 20, 's' if glob_count > 21 else ''))
        for elem in glob_list[-10:]:
            print(elem)
    else:
        for elem in glob_list:
            print(elem)
    print('Total elements found: {}'.format(glob_count))


def main():
    parser = ArgumentParser()
    parser.add_argument('glob')
    parser.add_argument('-a', '--all', action='store_true', help='If selected show all found elements')
    args = parser.parse_args()

    ll_glob(args.glob, show_all=args.all)


if __name__ == '__main__':
    main()
