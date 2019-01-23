#!/usr/bin/env python3

"""
Tests for llglob.py
For test_ll_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'


import glob
from os.path import join
import subprocess
import unittest

from TD_file_utils.llglob import INTERVAL_MSG, TOTAL_MSG, ll_glob

from .generate_test_data import generate_data
from .source import GLOBS, check_command_installed, check_command_usage, clean, stdout_wrapper, stdout_to_list


class TestLLGlob(unittest.TestCase):
    cmd = 'llglob'
    src_data_dir = 'test_src'

    def setUp(self):
        clean(self.src_data_dir)
        generate_data(self.src_data_dir)

    def tearDown(self):
        clean(self.src_data_dir)

    def test_ll_glob(self):
        # src_data_dir = 'test_src'
        for glb in GLOBS:
            data = sorted(glob.glob(join(self.src_data_dir, glb)))

            test_data_all = stdout_wrapper(ll_glob, join(self.src_data_dir, glb), show_all=True).strip().split('\n')

            test_data = stdout_wrapper(ll_glob, join(self.src_data_dir, glb)).strip().split('\n')

            self.check_result(data, test_data, test_data_all)

    def test_ll_glob_command(self):
        # Package must be installed to system!
        # check command available in system
        check_command_installed(self.cmd)

        for glb in GLOBS:
            glb_path = join(self.src_data_dir, glb)
            data = sorted(glob.glob(glb_path))

            c = subprocess.Popen('{} "{}" -a'.format(self.cmd, glb_path), shell=True, stdout=subprocess.PIPE)
            test_data_all = stdout_to_list(c.communicate()[0].decode())

            c = subprocess.Popen('{} "{}"'.format(self.cmd, glb_path), shell=True, stdout=subprocess.PIPE)
            test_data = stdout_to_list(c.communicate()[0].decode())

            self.check_result(data, test_data, test_data_all)
        self.assertTrue(check_command_usage(self.cmd))

    def check_result(self, data, test_data, test_data_all):
        data_count = len(data)

        self.assertEqual(
            sorted(data) + [TOTAL_MSG.format(data_count)],
            test_data_all,
            [data, test_data_all]
        )

        interval_msg = INTERVAL_MSG.format(data_count - 20, 's' if data_count - 20 > 1 else '')
        if data_count > 20:
            new_data = data[:10] + [interval_msg] + data[-10:]
        else:
            new_data = data
        new_data += [TOTAL_MSG.format(len(data))]

        self.assertEqual(
            new_data,
            test_data
        )


if __name__ == '__main__':
    unittest.main()
