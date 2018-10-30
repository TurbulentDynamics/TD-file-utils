__author__ = "Nile ÓBroin"
__copyright__ = "Copyright 2018, TURBULENT DYNAMICS"

"""
Utility to check if there are any files missing in a sequence of steps

Args input "single glob"

Output
files present: [53-54,56-57...]
missing files: [51-52,55,58-60,63-66,69-70,73,76-77,79-81,84-88,90-101,103-124,126-127,129-133]


"""


import argparse
import os, glob, sys
from shutil import copyfile


parser = argparse.ArgumentParser(description='Process all files')

parser.add_argument('glob', help='glob')


#args = parser.parse_args()
args, unknown = parser.parse_known_args()


dir_list = glob.glob(args.glob)



steps = list()

for d in dir_list:
    u = d.split('_')
    i = u.index('step')
    step = int(u[i + 1])
    steps.append(step)

print(steps)

min_step = min(steps)
max_step = max(steps)

delta = (max_step - min_step) / len(steps)


full = range(min_step, max_step + delta, delta)
print full


for i in range(min_step, max_step + delta, delta):
    if i in full:
        index = full.index(i)
        full.pop(index)


print full
