#!/usr/bin/env python

from distutils.core import setup

# Read the required software from the list.
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='fangyan',
    version='1.0',
    description='GT Fangyan media project',
    author='Wyatt Lansford',
    packages=['fangyan_tones'],
    install_requires=[
        requirements
    ]
)