#!/usr/bin/env python3

"""
Tests for cpglob.py
For test_cp_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'

import glob
from os import makedirs
from os.path import isdir, isfile, join
import subprocess
import unittest

from TD_file_utils.cpglob import ERR_MSG, copy, copy_glob

from .generate_test_data import generate_data
from .source import GLOBS, check_command_installed, check_command_usage, check_glob, clean, stdout_wrapper


class TestCopyGlob(unittest.TestCase):
    cmd = 'cpglob'
    src_data_dir = 'test_src'
    dst_data_dir = 'test_dst'
    src_data_file = 'test.txt'

    def setUp(self):
        clean(self.src_data_dir, self.dst_data_dir, self.src_data_file)

    def tearDown(self):
        clean(self.src_data_dir, self.dst_data_dir, self.src_data_file)

    def test_copy(self):
        invalid_file = 'invalid.txt'
        clean(invalid_file)

        # src not exists
        copy(invalid_file, self.dst_data_dir)
        self.assertFalse(isfile(join(self.dst_data_dir, invalid_file)))

        # create src file
        with open(self.src_data_file, 'w'):
            pass

        # result folder not exists
        self.assertRaises(IOError, copy, self.src_data_file, self.dst_data_dir)

        makedirs(self.dst_data_dir)

        # test copy file
        copy(self.src_data_file, self.dst_data_dir)
        self.assertTrue(isfile(join(self.dst_data_dir, self.src_data_file)))

        # copy file that already exists
        self.assertEqual(
            ERR_MSG.format(join(self.dst_data_dir, self.src_data_file)),
            stdout_wrapper(copy, self.src_data_file, self.dst_data_dir).strip()
        )

        # test copy dir
        makedirs(self.src_data_dir)
        copy(self.src_data_dir, self.dst_data_dir)
        self.assertTrue(isdir(join(self.dst_data_dir, self.src_data_dir)))

        # copy dir that already exists
        self.assertEqual(
            ERR_MSG.format(join(self.dst_data_dir, self.src_data_dir)),
            stdout_wrapper(copy, self.src_data_dir, self.dst_data_dir).strip()
        )

    def test_copy_glob(self):
        generate_data(self.src_data_dir)
        for glb in GLOBS:
            data = glob.glob(join(self.src_data_dir, glb))
            copy_glob(join(self.src_data_dir, glb), self.dst_data_dir)
            check_glob(self.src_data_dir, self.dst_data_dir, data)
            clean(self.dst_data_dir)
            makedirs(self.dst_data_dir)

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


if __name__ == '__main__':
    unittest.main()
