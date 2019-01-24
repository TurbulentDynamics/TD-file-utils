#!/usr/bin/env python3

__author__ = "Nile ÓBroin, Alexander Kovalenko, Boris Polyanskiy"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to generate thousands of files to test utilities
Alias for tests.generate_test_data.generate_data
"""

from argparse import ArgumentParser

from tests.generate_test_data import generate_data


def process_args():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', default='./', help='Result folder')
    parser.add_argument('--verbose', action='store_true', help='Print detail information about generating')

    return parser.parse_args()


def main():
    args = process_args()
    generate_data(args.output, verbose=args.verbose)


if __name__ == '__main__':
    main()
