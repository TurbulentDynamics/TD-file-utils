#!/usr/bin/env python3

"""
Tests for rmglob.py
For test_rm_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'


import glob
from os import makedirs
from os.path import abspath, isdir, join
import subprocess
import unittest

from TD_file_utils.rmglob import find_dirs, remove, remove_glob
from TD_file_utils.stuff import CPU_COUNT

from .generate_test_data import generate_data
from .source import GLOBS, clean, check_command_installed, check_command_usage, check_not_glob, stdout_wrapper


class TestRemoveGlob(unittest.TestCase):
    cmd = 'rmglob'
    src_data_file = 'test.txt'
    src_data_dir = 'test_src'

    def setUp(self):
        clean(self.src_data_dir)

    def tearDown(self):
        clean(self.src_data_dir)

    def test_remove(self):
        invalid_file = 'invalid.txt'
        clean(invalid_file)

        # src not exists
        self.assertRaises(IOError, remove, invalid_file)

        # create src file
        with open(self.src_data_file, 'w'):
            pass

        # test rm file
        self.assertRaises(NotADirectoryError, remove, self.src_data_file)
        clean(self.src_data_file)

        # test move dir
        makedirs(self.src_data_dir)
        remove(self.src_data_dir)
        self.assertFalse(isdir(self.src_data_dir))

    def test_remove_glob(self):
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            data = glob.glob(join(self.src_data_dir, glb))
            stdout_wrapper(remove_glob, join(self.src_data_dir, glb), CPU_COUNT)
            self.assertTrue(check_not_glob(join(self.src_data_dir, glb), data))

    def test_rm_glob_command(self):
        check_command_installed(self.cmd)
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            data = glob.glob(join(self.src_data_dir, glb))
            subprocess.call('{} "{}"'.format(self.cmd, join(self.src_data_dir, glb)), shell=True)
            self.assertTrue(check_not_glob(join(self.src_data_dir, glb), data))

        # check call without arguments
        self.assertTrue(check_command_usage(self.cmd))

    def test_find_dirs(self):
        generate_data(self.src_data_dir)
        for glb in GLOBS:
            glb_path = join(self.src_data_dir, glb)
            data = [abspath(x) for x in glob.iglob(glb_path) if isdir(x)]
            self.assertEqual(list(find_dirs(glb_path)), data)


if __name__ == '__main__':
    unittest.main()
