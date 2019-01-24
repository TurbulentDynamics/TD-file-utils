#!/usr/bin/env python3

"""
Tests for break_step.py
For test_break_step_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'

import glob
from os import listdir, makedirs
from os.path import join
import re
import subprocess
import unittest

from TD_file_utils.break_step import break_step, calculate_interval, get_element

from .generate_test_data import generate_data
from .source import GLOBS, clean, check_command_usage, check_command_installed, check_not_glob


class TestBreakStep(unittest.TestCase):
    cmd = 'break_step'
    src_data_dir = 'test_src'

    def setUp(self):
        clean(self.src_data_dir)

    def tearDown(self):
        clean(self.src_data_dir)

    def test_calculate_interval(self):
        test_data = [
            ((3, 0, 2), 2),     # regular call
            ((2, 0, 2), 2),
            ((4, 0, 2), 4),
            ((3, 3, 2), 3),     # num equal start
            ((3, 0, -2), 2),    # negative step
            ((4, 8, 2), 4),     # num less than start
            ((5, 8, 2), 4),
            ((5, 9, 3), 3),
            ((10000001, 0, 2), 10000000)

        ]
        for args, answer in test_data:
            self.assertEqual(calculate_interval(*args), answer)
        self.assertRaises(ValueError, calculate_interval, *(3, 6, 0))   # zero interval

    def test_get_element(self):
        generate_data(self.src_data_dir)
        for glb in GLOBS:
            glob_path = join(self.src_data_dir, glb)

            self.assertEqual(len(glob.glob(glob_path)), len(list(get_element(glob_path, 100))))

            for glob_step in (10, 13, 20, 39, 50, 100, 200, 500, -100):
                for src, dst in get_element(glob_path, glob_step):
                    found = re.search(r'_(\d+)_(\d+)$', dst)
                    # Check border in dst path
                    self.assertTrue(found)
                    left_border, right_border = found.groups()
                    # Check interval correct
                    self.assertTrue(int(right_border) - int(left_border) + 1 == abs(glob_step))
                    # Check step in interval
                    step_found = re.search(r'step_(\d{8})', src)
                    step, *_ = step_found.groups()
                    self.assertTrue(int(left_border) <= int(step) <= int(right_border))
        clean(self.src_data_dir)
        # Check non-step call
        for new_dir in (self.src_data_dir, join(self.src_data_dir, 'plot_slice_step_cut_1026')):
            makedirs(new_dir)
            self.assertEqual(list(get_element(self.src_data_dir + '/*', 20)), [])
        with self.assertRaises(ValueError):
            list(get_element('./*', 0))

    def test_break_step(self):
        for glb in GLOBS:
            generate_data(self.src_data_dir)
            glob_path = join(self.src_data_dir, glb)
            data = glob.glob(glob_path)
            break_step(glob_path, 100)

            self.check_result(data, glb)

    def test_break_step_command(self):
        check_command_installed(self.cmd)

        for glb in GLOBS:
            generate_data(self.src_data_dir)
            glob_path = join(self.src_data_dir, glb)
            data = glob.glob(glob_path)
            subprocess.call('{} "{}" {}'.format(self.cmd, join(self.src_data_dir, glb), 100), shell=True)

            self.check_result(data, glb)
        # check call without arguments
        self.assertTrue(check_command_usage(self.cmd))

    def check_result(self, data, glb):
        self.assertTrue(check_not_glob(join(self.src_data_dir, glb), data))
        tmp = []
        for path in listdir(self.src_data_dir):
            for src in listdir(join(self.src_data_dir, path)):
                tmp.append(join(self.src_data_dir, src))
                self.assertIn(join(self.src_data_dir, src), data)
        for g in data:
            self.assertIn(g, tmp)
        clean(self.src_data_dir)


if __name__ == '__main__':
    unittest.main()
