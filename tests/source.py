#!/usr/bin/env python3

__author__ = 'Boris Polyanskiy'

from io import StringIO
import glob
from os import listdir, remove
from os.path import abspath, dirname, isdir, isfile, join
from shutil import rmtree
import subprocess
import sys
import unittest

GLOBS = ('plot_slice_*', 'plot_axis_*', 'plot_rotational_*', 'plot_zero_*', '*cut_1536', '*step_*40_*', '*step_*100_*')


def clean(*args):
    """Deletes all files and folders in args"""
    for arg in args:
        if isfile(arg):
            remove(arg)
        elif isdir(arg):
            rmtree(arg)


def stdout_wrapper(func, *args, **kwargs):
    """Call func with redirected stdout and return output."""
    with StringIO() as log:
        tmp, sys.stdout = sys.stdout, log
        func(*args, **kwargs)
        sys.stdout = tmp
        return log.getvalue()


def check_glob(src, dst, data):
    """Check dst folder exists and listdir in dst equals with data."""
    return isdir(dst) and sorted(data) == sorted(join(src, x) for x in listdir(dst))


def check_not_glob(src, data):
    """Check each element in data not in src glob."""
    return all(x not in data for x in glob.glob(src))


def check_command_installed(cmd):
    """Try to call selected cmd and return True. If command not installed to system raise unittest.SkipTest"""
    try:
        subprocess.call(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return True
    except IOError:
        install_str = 'python {} install'.format(abspath(join(dirname(__file__), '..', 'setup.py', )))
        raise unittest.SkipTest('Install package TD-file-utils first!\nFor installing type: {}'.format(install_str))


def check_command_usage(cmd):
    """Check that selected command output contain word 'usage'."""
    # check call without arguments
    c = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    return b'usage' in c.communicate()[1]


def stdout_to_list(stdout):
    """Convert stdout (str) to list of stripped strings"""
    return [x.strip() for x in stdout.split('\n') if x.strip()]
