#!/usr/bin/env python3

#!/usr/bin/env python3
__author__ = "Nile ÓBroin"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to generate thousands of files to test utilities
"""


import os



SLICE = "plot_slice_step_%08i_cut_1026"
AXIS = "plot_axis__step_%08i_cut_1536"
ROTATION = "plot_rotational_capture_angle_%i_step_%08i_impeller_id_%i"
ZERO = "plot_zero_deg_axis_capture_imp_passed_%i_step_%08i"

def pymkdir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory %s created" % dirName)
    else:
        print("Directory %s already exists" % dirName)



for s in range(0, 600, 20):
    pymkdir(SLICE % s)
    pymkdir(AXIS % s)

for s in range(0, 600, 50):
    for i in range(0, 6):
        pymkdir(ROTATION % (15, s, i))

for s in range(0, 600, 13):
    pymkdir(ZERO % (15, s))
