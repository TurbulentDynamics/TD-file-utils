#!/usr/bin/env python3

"""
Some useful multiprocessing utilities. Used by other package modules.
"""

__author__ = 'Boris Polyanskiy'

from multiprocessing import Process, Queue, cpu_count

CPU_COUNT = cpu_count()


def worker(queue, func):
    """Queue worker.
    Polls the `queue`, if found element in queue - call `func` with unpacked element.
    If found `None` in queue - stop polling.

    :param queue: multiprocessing Queue
    :param func: function to call
    :return: None
    """

    while True:
        item = queue.get()
        if item is None:
            break
        func(*item)


def pool(func, it, proc_count):
    """Multiprocessing pool.
    Create `proc_count` count of processes, put arguments by `it` to queue.

    :param func: function to call.
    :param it: iterable, that contain func's arguments (as tuple).
    :param proc_count: count of processes.
    :return: None
    """

    queue = Queue()

    threads = []
    for x in range(proc_count):
        t = Process(target=worker, args=(queue, func))
        t.start()
        threads.append(t)
    for elem in it:
        queue.put(elem)
    for i in range(proc_count):
        queue.put(None)
    for t in threads:
        t.join()
