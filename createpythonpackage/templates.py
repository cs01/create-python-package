readme = """# {name}

"""

setup = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setuptools is a fully-featured, actively-maintained, and stable
# library designed to facilitate packaging Python projects.
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such as the name and version)
# as well as which code files to include.
# https://packaging.python.org/tutorials/packaging-projects/
# https://setuptools.readthedocs.io/en/latest/

import ast
import io
import re
import os
import sys
from setuptools import find_packages, setup, Command

DEPENDENCIES = []
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version() -> str:
    main_file = os.path.join(CURDIR, "{name}", "main.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="{name}",
    version=get_version(),
    author="{author}",
    author_email="{email}",
    description="description",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/username/project",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={{
        # "console_scripts": ["sample=sample:main",]
    }},
    zip_safe=False,
    install_requires=DEPENDENCIES,
    python_requires=">=3.6",
    # license and classifier list:
    # https://pypi.org/pypi?%%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

"""

main = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "{version}"


def main():
    print("TODO")


if __name__ == "__main__":
    main()

"""

gitignore = """*.pyc
venv/
activate-venv
bin/
build/
develop-eggs/
dist/
eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
"""

licence = """MIT License

Copyright (c) {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

makefile = """.PHONY: clean build publish

build: clean
	python3 -m pip install --upgrade --quiet setuptools wheel twine
	python3 setup.py --quiet sdist bdist_wheel

publish: build
	python3 -m twine upload dist/*

clean:
	rm -r build dist *.egg-info || true
"""
