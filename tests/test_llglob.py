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
from .source import GLOBS, check_command_installed, clean, stdout_wrapper


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
            data_count = len(data)
            test_data_all = stdout_wrapper(ll_glob, join(self.src_data_dir, glb), show_all=True).split('\n')
            self.assertEqual(
                sorted(data) + [TOTAL_MSG.format(data_count), ''],
                test_data_all
            )
            test_data = stdout_wrapper(ll_glob, join(self.src_data_dir, glb)).split('\n')

            interval_msg = INTERVAL_MSG.format(data_count - 20, 's' if data_count - 20 > 1 else '')
            if data_count > 20:
                new_data = data[:10] + [interval_msg] + data[-10:]
            else:
                new_data = data
            new_data += [TOTAL_MSG.format(len(data)), '']

            self.assertEqual(
                new_data,
                test_data
            )

    def test_ll_glob_command(self):
        def stdout_to_list(stdout):
            return [x.strip() for x in stdout.strip().split('\n')]

        # Package must be installed to system!
        # check command available in system
        check_command_installed(self.cmd)

        for glb in GLOBS:
            glb_path = join(self.src_data_dir, glb)
            data = sorted(glob.glob(glb_path))
            data_count = len(data)

            c = subprocess.Popen('{} "{}" -a'.format(self.cmd, glb_path), shell=True, stdout=subprocess.PIPE)
            test_data_all = stdout_to_list(c.communicate()[0].decode())
            self.assertEqual(
                sorted(data) + [TOTAL_MSG.format(data_count)],
                test_data_all
            )

            c = subprocess.Popen('{} "{}"'.format(self.cmd, glb_path), shell=True, stdout=subprocess.PIPE)
            test_data = stdout_to_list(c.communicate()[0].decode())

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
