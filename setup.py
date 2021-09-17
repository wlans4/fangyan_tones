#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Fangyan',
    version='0.1',
    description='GT Fangyan media project',
    author='Wyatt Lansford',
    packages=['fangyan_tones'],
    install_requires=[
        'pypinyin'
    ]
)