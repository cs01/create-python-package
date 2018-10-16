#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from setuptools import find_packages, setup, Command

DEPENDENCIES = []
CURDIR = os.path.abspath(os.path.dirname(__file__))
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="create-python-package",
    version="0.0.0.5",
    author="Chad Smith",
    author_email="grassfedcode@gmail.com",
    description="Create the file and folder structure for a Python package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cs01/create-python-package",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=["package", "setup"],
    scripts=[],
    entry_points={
        "console_scripts": [
            "create-python-package = createpythonpackage.main:create",
            "publish-python-package = createpythonpackage.main:publish",
        ]
    },
    extras_require={},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
