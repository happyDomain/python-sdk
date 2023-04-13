#!/usr/bin/env python3

import os
import re
from glob import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.0.2"

setup(
    name = "happydomain",
    version = version,
    description = "Finally a simple interface for domain names.",
    long_description = open('README.md').read(),

    author = "happyDomain's team",
    author_email = 'contact+pypi@happydomain.org',

    url = 'https://git.happydomain.org/python-sdk',
    license = 'CECILL-2.1',

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Topic :: Internet :: Name Service (DNS)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',

        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
    ],

    keywords = 'dns ns happydomain domain domainname',

    provides = ['happydomain'],

    install_requires=['requests'],

    packages=[
        'happydomain',
    ],
)
