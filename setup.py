#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

from abvdget import __version__

setup(
    name='abvdget',
    version=__version__,
    description="abvdget - download data from the Austronesian Basic Vocabulary Database",
    url='',
    author='Simon J. Greenhill',
    author_email='simon@simon.net.nz',
    license='BSD',
    zip_safe=True,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='austronesian data API',
    packages=find_packages(),
    install_requires=['requests', ],
    entry_points={
        'console_scripts': [
            'abvd_download = abvdget.abvd_download:main'
        ],
    },
    test_suite="abvdget.tests",
)
