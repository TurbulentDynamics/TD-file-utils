#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    version='1.0.4',
    name='TD_file_utils',
    entry_points={
        'console_scripts': [
            'cpglob=TD_file_utils.cpglob:main',
            'mvglob=TD_file_utils.mvglob:main',
            'rmglob=TD_file_utils.rmglob:main',
            'llglob=TD_file_utils.llglob:main',
            'break_step=TD_file_utils.break_step:main',
            'check_step_integrity=TD_file_utils.check_step_integrity:main'
        ],
    },
    packages=find_packages('.', exclude=['tests'])
)
