#!/usr/bin/env python3

"""
Utility to move dirs/files via glob pattern.
Multiprocessing. To set count of processes use '-n' parameter. Default processes count - count of CPU at host PC.
Result folder will be created.
Sample of call:
    python mvglob.py test/plot_axis_* new_folder -n 8
"""

__author__ = 'Boris Polyanskiy'

from argparse import ArgumentParser
import glob
import itertools
from os import getpid, makedirs
from os.path import basename, exists, isdir, join
import shutil

from TD_file_utils.stuff import CPU_COUNT, pool

ERR_MSG = 'Already exists: {}'


def move(src, dst):
    """Move source file/folder to destination folder. Not overwrite if file/folder exists.

    Destination path will include basename of source path.

    :param src: path to source file/folder.
    :param dst: path to result folder.
    :return: None.
    """

    res = join(dst, basename(src))
    # print("[PID: %6d] move %s -> %s" % (getpid(), src, res))

    if exists(src):
        if exists(res):
            print(ERR_MSG.format(res))
        else:
            shutil.move(src, res)


def move_glob(glb, dst, proc_count=8):
    """Move all files/folders matching pattern to destination.

    :param glb: pattern (glob).
    :param dst: destination folder.
    :param proc_count: count of processes.
    :return: None.
    """

    if not isdir(dst):
        makedirs(dst)
    pool(move, itertools.zip_longest(glob.iglob(glb), (), fillvalue=dst), proc_count)


def main():
    parser = ArgumentParser(description='Utility to move dirs/files via glob pattern.')
    parser.add_argument('glob', help='Shell glob expression, quoted')
    parser.add_argument('new_dir', help='Result folder')
    parser.add_argument('-n', '--numprocs', type=int, help='Process count (default: 8)', default=CPU_COUNT)
    args = parser.parse_args()

    move_glob(args.glob, args.new_dir, args.numprocs)


if __name__ == '__main__':
    main()
