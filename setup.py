#!/usr/bin/env python
import io
import os
from setuptools import find_packages, setup  # type: ignore
from pathlib import Path
import ast
import re

CURDIR = Path(__file__).parent

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
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    keywords=["package", "setup"],
    scripts=[],
    entry_points={
        "console_scripts": ["create-python-package = createpythonpackage.main:main"]
    },
    install_requires=["cookiecutter"],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)
