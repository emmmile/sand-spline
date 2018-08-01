#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import os
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


#####
# Helper functions
#####
def read(*filenames, **kwargs):
    """
    Build an absolute path from ``*filenames``, and  return contents of
    resulting file.  Defaults to UTF-8 encoding.
    """
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for fl in filenames:
        with codecs.open(os.path.join(HERE, fl), "rb", encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    re_str = r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta)
    meta_match = re.search(re_str, META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def install_requires():
    reqs_txt = read("requirements.txt")
    parsed = reqs_txt.split("\n")
    return [r for r in parsed if len(r) > 0]


#####
# Project-specific constants
#####
NAME = "sand-spline"
META_PATH = os.path.join(NAME, "__init__.py")
META_FILE = read(META_PATH)

setup(
    name=NAME,
    version=find_meta("version"),
    description=find_meta("description"),
    author=find_meta("author"),
    author_email=find_meta("email"),
    packages=find_packages(exclude=["tests*", "res/*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=install_requires()
)
