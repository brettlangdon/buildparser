#!/usr/bin/env python

from setuptools import setup, find_packages

from buildparser import __version__

setup(
    name="buildparser",
    version=__version__,
    description="Generic job build specification parser",
    author="Brett Langdon",
    author_email="brett@blangdon.com",
    url="https://github.com/brettlangdon/buildparser",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "PyYAML==3.11",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ]
)
