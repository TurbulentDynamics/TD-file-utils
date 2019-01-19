#!/usr/bin/env python3

__author__ = "Nile ÓBroin, Alexander Kovalenko"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to delete thousands of files
Should take only 1 glob as input
"""

import argparse
import os, glob, sys
import multiprocessing
from multiprocessing import Pool
from shutil import rmtree
import itertools
from itertools import islice, takewhile, repeat

NUM_PROCS = 8

def find_dirs(glb):
    for x in glob.iglob(glb):
        d = os.path.realpath(x)
        if os.path.isdir(d):
            yield d

def remove(dirname):
    print("[PID: %d] Removing %s" % (os.getpid(), dirname))
    rmtree(dirname)

def remove_glob(glb, numprocs):
    chunkify = (lambda it, n: takewhile(bool, (list(islice(it, n)) for _ in repeat(None))))
    chunks = chunkify(iter(find_dirs(glb)), numprocs)
    pool = Pool(processes=numprocs)
    for chunk in chunks: pool.map(remove, chunk)


def main():
    parser = argparse.ArgumentParser(description='Utility to delete thousands of files.')
    parser.add_argument('glob', help='Shell glob expression, quoted')
    parser.add_argument('-n', '--numprocs', type=int, help='Process count (default: 8)', default=NUM_PROCS)
    args = parser.parse_args()

    remove_glob(args.glob, args.numprocs)


if __name__ == '__main__':
    main()

