#!/usr/bin/env python3
__author__ = "Nile ÓBroin"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to copy png files within a directory structure to a single directory
"""

import argparse
import os, glob, sys
from shutil import copyfile


parser = argparse.ArgumentParser(description='Process all files')

#parser.add_argument("dst", help="destination directory")
parser.add_argument('glob', help='globs')


#args = parser.parse_args()
args, unknown = parser.parse_known_args()


dir_list = glob.glob(args.glob)



#PLOT_slice/plot_slice_Q4_step_00088980_cut_129/Q4-uxyz-log-vort-contour.png


def remove_step_num(plt_dir):
    parts = plt_dir.split('_')
    i = parts.index('step')
    parts.pop(i)
    parts.pop(i)
    return "_".join(parts)





def copy_src(src):
    path = src.replace('-', '_').replace('.', '_').split('/')

    dst_dir = "%s_%s" % (remove_step_num(path[-2]), path[-1])

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    dst_filename = "%s_%s.png" % (path[-2], path[-1][:-4])
    dst = os.path.join(dst_dir, dst_filename)


    if os.path.isfile(dst):
        print("File exists", dst)
    else:
        print(src, " -> ", dst)
        copyfile(src, dst)


for file_or_dir in dir_list:
    if file_or_dir.endswith('png'):
        copy_src(d)
        continue
    for src in glob.glob(file_or_dir + "/*.png"):
        copy_src(src)
