#!/usr/bin/env python3

"""
Tests for stuff.py
"""

__author__ = 'Boris Polyanskiy'


from os.path import isfile
from multiprocessing import Process, Queue
from time import sleep
import unittest

from TD_file_utils.stuff import pool, worker

from .source import clean


def writer(path, string):
    """Add string to file at path

    File must exist.

    :param path: path to file
    :param string: string for writing to file
    :return: None
    """

    with open(path, 'a') as stream:
        print(string, file=stream)


def read_file(path):
    """Read file at path, return list of stripped strings.

    :param path: path to file
    :return: list with stripped strings
    """
    with open(path) as stream:
        return [x.strip() for x in stream.readlines()]


class TestStuff(unittest.TestCase):
    data_src_file = 'test.txt'
    test_strings = ['hello', 'world', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet']

    def tearDown(self):
        clean(self.data_src_file)

    def test_worker(self):

        with open('test.txt', 'w'):
            pass

        test_strings_2 = self.test_strings + ['python']

        queue = Queue()
        p = Process(target=worker, args=(queue, writer))
        p.start()

        # Check queue work
        for string in self.test_strings:
            queue.put((self.data_src_file, string))
        sleep(0.5)
        self.assertEqual(read_file(self.data_src_file), self.test_strings)

        # Check additional adding
        queue.put((self.data_src_file, 'python'))
        sleep(0.5)
        self.assertEqual(read_file(self.data_src_file), test_strings_2)

        # Check stop
        queue.put(None)
        sleep(0.5)
        self.assertEqual(read_file(self.data_src_file), test_strings_2)

        p.join()
        self.assertEqual(read_file(self.data_src_file), test_strings_2)

    def test_pool(self):
        test_files = ['test_{}.txt'.format(x) for x in range(len(self.test_strings))]
        clean(*test_files)

        pool(writer, zip(test_files, self.test_strings), 4)
        for string, test_file in zip(self.test_strings, test_files):
            self.assertTrue(isfile(test_file))
            self.assertEqual(read_file(test_file), [string])
        clean(*test_files)

        # Check count of data less than count of processes
        test_data = ['test1', 'test2']
        test_files = ['test_{}.txt'.format(x) for x in range(len(test_data))]
        clean(*test_files)
        pool(writer, zip(test_files, test_data), 8)
        for string, test_file in zip(test_data, test_files):
            self.assertTrue(isfile(test_file))
            self.assertEqual(read_file(test_file), [string])
        clean(*test_files)


if __name__ == '__main__':
    unittest.main()
