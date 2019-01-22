#!/usr/bin/env python3

"""
Tests for cpglob.py
For test_cp_glob_command required TD-file-utils package installed to system.
"""

__author__ = 'Boris Polyanskiy'

import glob
from io import StringIO
from os import listdir, makedirs, remove
from os.path import abspath, dirname, isdir, isfile, join
from shutil import rmtree
import subprocess
import sys
import unittest

from TD_file_utils.cpglob import copy, copy_glob

from .generate_test_data import generate_data


GLOBS = ('plot_slice*', '*cut_1536', '*step_*40_*', '*step_*100_*')


def clean(*args):
    for arg in args:
        if isfile(arg):
            remove(arg)
        elif isdir(arg):
            rmtree(arg)


class TestCopyGlob(unittest.TestCase):
    def check_glob(self, src, dst, glb):
        self.assertTrue(isdir(dst))
        self.assertEqual(
            sorted(glob.glob(join(src, glb))),
            sorted(join(src, x) for x in listdir(dst))
        )

    def test_copy(self):
        def copy_with_log(src, dst):
            with StringIO() as log:
                tmp, sys.stdout = sys.stdout, log
                copy(src, dst)
                sys.stdout = tmp
                return log.getvalue()

        src_file = 'test.txt'
        src_dir = 'test_dir'
        invalid_file = 'invalid.txt'
        result_dir = 'test_result'

        clean(src_file, src_dir, result_dir, invalid_file)

        # src not exists
        copy(invalid_file, result_dir)
        self.assertFalse(isfile(join(result_dir, invalid_file)))

        # create src file
        with open(src_file, 'w'):
            pass

        # result folder not exists
        self.assertRaises(FileNotFoundError, copy, src_file, result_dir)

        makedirs(result_dir)

        # test copy file
        copy(src_file, result_dir)
        self.assertTrue(isfile(join(result_dir, src_file)))

        # copy file that already exists
        self.assertEqual(
            'Already exists: {}'.format(join(result_dir, src_file)),
            copy_with_log(src_file, result_dir).strip()
        )

        # test copy dir
        makedirs(src_dir)
        copy(src_dir, result_dir)
        self.assertTrue(isdir(join(result_dir, src_dir)))

        # copy dir that already exists
        self.assertEqual(
            'Already exists: {}'.format(join(result_dir, src_dir)),
            copy_with_log(src_dir, result_dir).strip()
        )

        clean(src_file, src_dir, result_dir, invalid_file)

    def test_copy_glob(self):
        src_data_dir = 'test_src'
        new_data_dir = 'test_dst'
        clean(src_data_dir, new_data_dir)

        generate_data(src_data_dir)
        for glb in GLOBS:
            copy_glob(join(src_data_dir, glb), new_data_dir)
            self.check_glob(src_data_dir, new_data_dir, glb)
            rmtree(new_data_dir)
            makedirs(new_data_dir)
        clean(src_data_dir, new_data_dir)

    def test_cp_glob_command(self):
        # Package must be installed to system!
        # check command available in system
        try:
            subprocess.call('cpglob', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            install_str = 'python {} install'.format(abspath(join(dirname(__file__), '..', 'setup.py',)))
            raise unittest.SkipTest('Install package TD-file-utils first!\nFor installing type: {}'.format(install_str))

        src_data_dir = 'test_src'
        new_data_dir = 'test_dst'
        clean(src_data_dir, new_data_dir)

        generate_data(src_data_dir)

        for glb in GLOBS:
            subprocess.call('cpglob "{}" {}'.format(join(src_data_dir, glb), new_data_dir), shell=True)
            self.check_glob(src_data_dir, new_data_dir, glb)
            rmtree(new_data_dir)

        # check call without arguments
        c = subprocess.Popen('cpglob', shell=True, stderr=subprocess.PIPE)
        self.assertIn(b'usage', c.communicate()[1])

        clean(src_data_dir, new_data_dir)


if __name__ == '__main__':
    unittest.main()
