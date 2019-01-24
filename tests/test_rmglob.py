#!/usr/bin/env python3

"""
Tests for rmglob.py
For test_rm_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'


import glob
from os import makedirs
from os.path import isdir, isfile, join
import subprocess
import unittest

from TD_file_utils.rmglob import remove, remove_glob
from TD_file_utils.stuff import CPU_COUNT

from .generate_test_data import generate_data
from .source import GLOBS, clean, check_command_installed, check_command_usage, check_not_glob, stdout_wrapper


class TestRemoveGlob(unittest.TestCase):
    cmd = 'rmglob'
    src_data_file = 'plot_slice_00000000.txt'
    src_data_dir = 'test_src'

    def setUp(self):
        clean(self.src_data_dir)

    def tearDown(self):
        clean(self.src_data_dir)

    def test_remove(self):
        # create src file
        with open(self.src_data_file, 'w'):
            pass

        # test rm file
        remove(self.src_data_file)
        self.assertFalse(isfile(self.src_data_file))

        # test rm file that not exists
        remove(self.src_data_file)

        # test rm dir
        makedirs(self.src_data_dir)
        remove(self.src_data_dir)
        self.assertFalse(isdir(self.src_data_dir))

    def test_remove_glob(self):
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            with open(join(self.src_data_dir, self.src_data_file), 'w'):
                pass
            data = glob.glob(join(self.src_data_dir, glb))
            stdout_wrapper(remove_glob, join(self.src_data_dir, glb), CPU_COUNT)
            self.assertTrue(check_not_glob(join(self.src_data_dir, glb), data))

    def test_rm_glob_command(self):
        check_command_installed(self.cmd)
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            with open(join(self.src_data_dir, self.src_data_file), 'w'):
                pass
            data = glob.glob(join(self.src_data_dir, glb))
            subprocess.call('{} "{}"'.format(self.cmd, join(self.src_data_dir, glb)), shell=True)
            self.assertTrue(check_not_glob(join(self.src_data_dir, glb), data))

        # check call without arguments
        self.assertTrue(check_command_usage(self.cmd))


if __name__ == '__main__':
    unittest.main()
