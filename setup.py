#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

if sys.version_info < (3, 6, 0):
    print("Python 3.6+ is required")
    exit(1)
from setuptools import find_packages, setup  # noqa E402
from pathlib import Path  # noqa E402
from typing import List  # noqa E402
import ast  # noqa E402
import re  # noqa E402

DEPENDENCIES = ["jinja2<2.20, >2.0"]
CURDIR = Path(__file__).parent
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version() -> str:
    main_file = CURDIR / "createpythonpackage" / "main.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="create-python-package",
    version=get_version(),
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
            "create-python-package = createpythonpackage.main:create_package"
        ]
    },
    install_requires=DEPENDENCIES,
    extras_require={"dev": ["black", "flake8", "mypy"]},
    test_suite="tests.test_createpythonpackage",
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
