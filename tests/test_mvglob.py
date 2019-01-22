#!/usr/bin/env python3

"""
Tests for mvglob.py
For test_mv_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'

import glob
from os import makedirs
from os.path import isdir, isfile, join
import unittest

from TD_file_utils.mvglob import ERR_MSG, move, move_glob

from .generate_test_data import generate_data
from .source import GLOBS, check_glob, clean, stdout_wrapper, SystemOperationTest


class TestMoveGlob(unittest.TestCase, SystemOperationTest):
    cmd = 'mvglob'
    src_data_file = 'test.txt'
    src_data_dir = 'test_src'
    dst_data_dir = 'test_dst'

    def setUp(self):
        clean(self.src_data_dir, self.dst_data_dir, self.src_data_file)

    def tearDown(self):
        clean(self.src_data_dir, self.dst_data_dir, self.src_data_file)

    def test_move(self):
        invalid_file = 'invalid.txt'
        clean(invalid_file)

        # src not exists
        move(invalid_file, self.dst_data_dir)
        self.assertFalse(isfile(join(self.dst_data_dir, invalid_file)))

        # create src file
        with open(self.src_data_file, 'w'):
            pass

        # result folder not exists
        self.assertRaises(IOError, move, self.src_data_file, self.dst_data_dir)

        makedirs(self.dst_data_dir)

        # test move file
        move(self.src_data_file, self.dst_data_dir)
        self.assertTrue(isfile(join(self.dst_data_dir, self.src_data_file)))

        # create src file
        with open(self.src_data_file, 'w'):
            pass
        # move file that already exists
        self.assertEqual(
            ERR_MSG.format(join(self.dst_data_dir, self.src_data_file)),
            stdout_wrapper(move, self.src_data_file, self.dst_data_dir).strip()
        )

        # test move dir
        makedirs(self.src_data_dir)
        move(self.src_data_dir, self.dst_data_dir)
        self.assertTrue(isdir(join(self.dst_data_dir, self.src_data_dir)))

        # move dir that already exists
        makedirs(self.src_data_dir)
        self.assertEqual(
            ERR_MSG.format(join(self.dst_data_dir, self.src_data_dir)),
            stdout_wrapper(move, self.src_data_dir, self.dst_data_dir).strip()
        )

    def test_move_glob(self):
        generate_data(self.src_data_dir)
        for glb in GLOBS:
            data = glob.glob(join(self.src_data_dir, glb))
            move_glob(join(self.src_data_dir, glb), self.dst_data_dir)
            check_glob(self.src_data_dir, self.dst_data_dir, data)
            clean(self.dst_data_dir)
            makedirs(self.dst_data_dir)


if __name__ == '__main__':
    unittest.main()
