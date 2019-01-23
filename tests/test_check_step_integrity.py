#!/usr/bin/env python3

"""
Tests for check_step_integrity.py
For test_check_step_integrity_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'

from os import makedirs
from os.path import join
import re
import subprocess
import unittest

from TD_file_utils.check_step_integrity import all_gaps, present_as_ranges, missing_as_ranges, get_steps, \
    check_step_integrity
from .generate_test_data import generate_data, SLISE_GAP, AXIS_GAP, ROTATION_GAP, ZERO_GAP
from .source import clean, stdout_wrapper, check_command_installed, check_command_usage, stdout_to_list

GLOBS = ('plot_slice_*', 'plot_axis_*', 'plot_rotational_*', 'plot_zero_*')
GAPS = (SLISE_GAP, AXIS_GAP, ROTATION_GAP, ZERO_GAP)
MISS = (60, 100, 50, 169)

SIZE_REGEX = re.compile(r'(\d+)$')
MISS_REGEX = re.compile(r'\[(\d+)\]$')

DELETE_SRC = (
    'plot_axis__step_00000100_cut_1536',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_0',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_1',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_2',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_3',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_4',
    'plot_rotational_capture_angle_15_step_00000050_impeller_id_5',
    'plot_slice_step_00000060_cut_1026',
    'plot_zero_deg_axis_capture_imp_passed_15_step_00000169'
)


class TestCheckStepIntegrity(unittest.TestCase):
    cmd = 'check_step_integrity'
    src_data_dir = 'test_src'

    def setUp(self):
        clean(self.src_data_dir)

    def tearDown(self):
        clean(self.src_data_dir)

    def test_all_gaps(self):
        self.assertEqual(list(all_gaps([5, 10, 15, 25, 35, 50, 100, 100])), [5, 5, 10, 10, 15, 50, 0])
        self.assertEqual(list(all_gaps([100, 100, 50, 35, 25, 15, 10, 5])), [0, -50, -15, -10, -10, -5, -5])

    def test_present_as_ranges(self):
        self.assertEqual(list(present_as_ranges([1, 2, 3, 4, 5, 6])), ['1-6'])
        self.assertEqual(list(present_as_ranges([1, 2, 6, 4, 5, 3])), ['1-2', '6', '4-5', '3'])
        self.assertEqual(list(present_as_ranges([])), [])
        self.assertEqual(list(present_as_ranges([0, 2, 4, 6, 8], 2)), ['0-8'])
        self.assertEqual(list(present_as_ranges([0, 2, 3, 6, 8], 2)), ['0-2', '2', '6-8'])
        with self.assertRaises(ZeroDivisionError):
            list(present_as_ranges([1, 2, 3], 0))

    def test_missing_as_ranges(self):
        self.assertEqual(list(missing_as_ranges([1, 2, 5, 6], 2)), ['2'])
        self.assertEqual(list(missing_as_ranges([1, 2, 7, 8, 9, 12], 2)), ['2-4', '10'])
        self.assertEqual(list(missing_as_ranges([1, 2, 7, 8, 9, 11, 12], 2)), ['2-4'])

    def test_get_steps(self):
        generate_data(self.src_data_dir)
        for glb in GLOBS:
            glob_path = join(self.src_data_dir, glb)
            steps = list(get_steps(glob_path))
            self.assertTrue(len(steps) > 0, glb)
            for step in steps:
                self.assertFalse(re.search(r'step_\d+', step))
                self.assertTrue(re.search(r'step_\*', step))
        clean(self.src_data_dir)
        makedirs(self.src_data_dir)
        self.assertEqual(list(get_steps(self.src_data_dir + '/*')), [])

    def test_check_step_integrity(self):
        generate_data(self.src_data_dir)
        for x in DELETE_SRC:
            clean(join(self.src_data_dir, x))

        self.assertTrue(len(GLOBS) == len(GAPS) == len(MISS), 'Invalid environment')

        for glb, gap, miss in zip(GLOBS, GAPS, MISS):
            glob_path = join(self.src_data_dir, glb)
            output = [x.strip() for x in stdout_wrapper(check_step_integrity, glob_path).split('\n') if x.strip()]
            self.check_output(output, gap, miss)

    def test_check_step_integrity_command(self):
        check_command_installed(self.cmd)
        generate_data(self.src_data_dir)
        for x in DELETE_SRC:
            clean(join(self.src_data_dir, x))

        self.assertTrue(len(GLOBS) == len(GAPS) == len(MISS), 'Invalid environment')

        for glb, gap, miss in zip(GLOBS, GAPS, MISS):
            glob_path = join(self.src_data_dir, glb)

            c = subprocess.Popen('{} "{}"'.format(self.cmd, glob_path), shell=True, stdout=subprocess.PIPE)
            output = stdout_to_list(c.communicate()[0].decode())

            self.check_output(output, gap, miss)
        self.assertTrue(check_command_usage(self.cmd))

    def check_output(self, output, gap, miss):
        self.assertTrue(output)
        gap_flag = False
        miss_flag = False
        for line in output:
            if 'Gap size' in line:
                size_found = SIZE_REGEX.search(line)
                self.assertTrue(size_found)
                size, *_ = size_found.groups()
                self.assertEqual(int(size), gap)
                gap_flag = True
            if 'Files missing' in line:
                miss_found = MISS_REGEX.search(line)
                self.assertTrue(miss_found)
                m, *_ = miss_found.groups()
                self.assertEqual(int(m), miss)
                miss_flag = True
        self.assertTrue(gap_flag)
        self.assertTrue(miss_flag)


if __name__ == '__main__':
    unittest.main()
