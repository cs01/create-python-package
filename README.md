<p align="center">
<a href="https://travis-ci.org/cs01/create-python-package"><img src="https://travis-ci.org/cs01/create-python-package.svg?branch=master" /></a>

<a href="https://pypi.python.org/pypi/pipx/">
<img src="https://img.shields.io/badge/pypi-0.2.0.0-blue.svg" /></a>
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# create-python-package
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/). Perfect for beginners and experts alike. Stop writing boilerplate and start coding.

Creates a battle-tested directory structure with `setup.py`. Also compatible with Pipenv. Generates a folder structure with a License, test directory, and more.

## Overview
This package ships with one CLI entrypoint, `create-python-package`.

To use create-python-package:
```
create-python-package mypackage
cd mypackage
```

## Installation
Python 3.6+ is required

### using pip
```
pip install --user create-python-package
```

### using pipx
*[pipx](https://github.com/pipxproject/pipx) allows you to run Python binaries into isolated virtual environments*
```
python3 -m pip install --user pipx
pipx ensurepath
```

You can run the latest version directly with
```
pipx run create-python-package
```

or install with

```
pipx install create-python-package
```


## Credits
Inspired by [create-react-app](https://github.com/facebook/create-react-app)
