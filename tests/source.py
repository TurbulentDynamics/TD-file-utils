#!/usr/bin/env python3

__author__ = 'Boris Polyanskiy'

from abc import ABCMeta, abstractmethod
from io import StringIO
import glob
from os import listdir, remove
from os.path import abspath, dirname, isdir, isfile, join
from shutil import rmtree
import subprocess
import sys
import unittest

from .generate_test_data import generate_data

GLOBS = ('plot_slice_*', 'plot_axis_*', 'plot_rotational_*', 'plot_zero_*', '*cut_1536', '*step_*40_*', '*step_*100_*')


def clean(*args):
    for arg in args:
        if isfile(arg):
            remove(arg)
        elif isdir(arg):
            rmtree(arg)


def stdout_wrapper(func, *args, **kwargs):
    with StringIO() as log:
        tmp, sys.stdout = sys.stdout, log
        func(*args, **kwargs)
        sys.stdout = tmp
        return log.getvalue()


def check_glob(src, dst, data):
    return isdir(dst) and sorted(data) == sorted(join(src, x) for x in listdir(dst))


def check_not_glob(src, data):
    return all(x not in data for x in glob.glob(src))


def check_command_installed(cmd):
    try:
        subprocess.call(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return True
    except IOError:
        install_str = 'python {} install'.format(abspath(join(dirname(__file__), '..', 'setup.py', )))
        raise unittest.SkipTest('Install package TD-file-utils first!\nFor installing type: {}'.format(install_str))


def check_command_usage(cmd):
    # check call without arguments
    c = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    return b'usage' in c.communicate()[1]


def stdout_to_list(stdout):
    return [x.strip() for x in stdout.split('\n') if x.strip()]


class SystemOperationTest:
    __meta__ = ABCMeta

    @property
    @abstractmethod
    def cmd(self): pass

    @property
    @abstractmethod
    def src_data_dir(self): pass

    @property
    @abstractmethod
    def dst_data_dir(self): pass

    def test_glob_command(self):
        # Package must be installed to system!
        # check command available in system
        check_command_installed(self.cmd)
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            data = glob.glob(join(self.src_data_dir, glb))
            subprocess.call('{} "{}" {}'.format(self.cmd, join(self.src_data_dir, glb), self.dst_data_dir), shell=True)
            self.assertTrue(check_glob(self.src_data_dir, self.dst_data_dir, data))
            clean(self.dst_data_dir)

        # check call without arguments
        self.assertTrue(check_command_usage(self.cmd))