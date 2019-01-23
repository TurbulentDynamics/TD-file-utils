#!/usr/bin/env python3

__author__ = "Nile ÓBroin, Alexander Kovalenko"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Functions to generate thousands of files to test utilities
"""

from os import makedirs
from os.path import isdir, join
import os

SLICE = "plot_slice_step_%08i_cut_1026"
AXIS = "plot_axis__step_%08i_cut_1536"
ROTATION = "plot_rotational_capture_angle_%i_step_%08i_impeller_id_%i"
ZERO = "plot_zero_deg_axis_capture_imp_passed_%i_step_%08i"

SLISE_GAP = AXIS_GAP = 20
ROTATION_GAP = 50
ZERO_GAP = 13


def pymkdir(dirName, verbose=False):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        if verbose:
            print("Directory %s created" % dirName)
    elif verbose:
        print("Directory %s already exists" % dirName)


def generate_data(dst='./', verbose=False):
    if not isdir(dst):
        makedirs(dst)

    for s in range(0, 600, 20):
        pymkdir(join(dst, SLICE % s), verbose)
        pymkdir(join(dst, AXIS % s), verbose)

    for s in range(0, 600, 50):
        for i in range(0, 6):
            pymkdir(join(dst, ROTATION % (15, s, i)), verbose)

    for s in range(0, 600, 13):
        pymkdir(join(dst, ZERO % (15, s)), verbose)
