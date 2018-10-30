#!/usr/bin/env python3
__author__ = "Nile ÓBroin"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to delete thousands of files

Should take only 1 glob as input
"""

import argparse
import os, glob, sys

NUM_FILES_PER_THREAD = 100
NUM_PROCS = 2


parser = argparse.ArgumentParser(description='Process all files')

parser.add_argument('glob', help='glob')

args, unknown = parser.parse_known_args()




def join_funcs(args, dir):


    # args = " ".join(dir)

    cmd = "rm -v " + dir
    print("Running %s" % cmd)

    #Add some Exception handling here
    subprocess.call(cmd, shell=True)






if __name__ == "__main__":
    if number of args > 1:
        print("Usage rmglob \"glob\*\"")
        exit(1)


    dir_list = find_dirs(args.globs)


    dir_pack = [dir_list[i:i + NUM_FILES_PER_THREAD] for i in range(0, len(dir_list), n)]


    if len(dir_list) < NUM_PROCS:
        NUM_PROCS = len(dir_list)


    with closing(multiprocessing.Pool(processes=NUM_PROCS, maxtasksperchild=10)) as p:
        p.starmap(join_funcs, zip(repeat(args), dir_pack))
