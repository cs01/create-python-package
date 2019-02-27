# create-python-package

<p>
<a href="https://travis-ci.org/cs01/create-python-package"><img src="https://travis-ci.org/cs01/create-python-package.svg?branch=master" /></a>

<a href="https://pypi.python.org/pypi/pipx/">
<img src="https://img.shields.io/badge/pypi-0.2.1.0-blue.svg" /></a>
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Overview
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/). Perfect for beginners and experts alike. Stop writing boilerplate and start coding.

Generates a project similar to the Python Packaging Authority's [sample project](https://github.com/pypa/sampleproject), but with various parts autogenerated based on your inputs.

### Features
* Creates a battle-tested directory structure with boilterplate for unit tests, license, [`setup.py`](https://github.com/pypa/sampleproject/blob/master/setup.py) and more
* Sets you up with popular Python environment managers such as venv and Pipenv
* Initializes a git repository for you with a .gitignore file

## Usage
This package ships with one CLI entrypoint, `create-python-package`.

To interactively answer questions about your project, such as author, license, etc.
```
$ create-python-package
```
You will then be prompted with questions such as
```
question version (0.0.0.1):
question description ():
question entry point (main.py):
question repository url ():
question author (Your Name):
question email (email@doman.com):
question environment management (venv) (options: venv, pipenv, poetry):
question license (mit) (options: mit, gplv3, apache2, bsd3):
```
These are used to populate setup.py and other files to give you as painless experience as possible when starting a new project.

To use defaults and skip interactive prompts, use the `--yes` flag
```
$ create-python-package --yes
```

## Installation
Python 3.6+ is required

### using pip
```
pip install --user create-python-package
```

### using pipx
*[pipx](https://github.com/pipxproject/pipx) allows you to run Python binaries directly, or install packages into isolated virtual environments and add their binaries to your PATH*
```
pipx run create-python-package
```

or install with

```
pipx install create-python-package
```

## Generated Directory Structure
```
>> pipx run create-python-package examplepackage --yes
>> tree -L 2 examplepackage/
examplepackage/
├── examplepackage
│   ├── __init__.py
│   └── main.py
├── LICENSE
├── makefile
├── MANIFEST.in
├── README.md
├── setup.py
├── tests
│   └── test_project.py
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    ├── pyvenv.cfg
    └── share
```

## Credits
Inspired by [create-react-app](https://github.com/facebook/create-react-app)
