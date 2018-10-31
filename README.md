<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# create-python-package
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/). Perfect for beginners and experts alike. No more guesswork!

Read more on the [blog post](https://medium.com/@grassfedcode/bringing-some-of-javascripts-packaging-solutions-to-python-1b02430d589e).

## Overview
This package ships with four CLI entrypoints:
```
- build-python-package
- create-python-package
- create-venv
- publish-python-package
```

To use create-python-package:
```
create-python-package mypackage
cd mypackage
source activate
```

To publish (which automatically builds first), run
```
publish-python-package path_to_package
```

To build without publishing
```
build-python-package path_to_package
````

To create a virtual environment
```
create-venv path  # creates venv at path/venv and symlink to activate at path/activate
# then run `source activate` to activate the virtual environment
````


## Virtualenv ready to go!
Inside the directory you can run
```
source activate
```
to activate an isolated Python environment that was created specifically for that package. To deactivate it, type
```
deactivate
```

To learn more about virtual environments, see [Creating Virtual Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments).

## Installation
*[pipx](https://github.com/cs01/pipx) is a new package that allows you to run or install Python binaries from packages*

```
pipx install create-python-package
```


>pipx install create-python-package
  installed package create-python-package, 0.0.0.5
  These binaries are now globally available
    - build-python-package
    - create-python-package
    - create-venv
    - publish-python-package
done! ✨ 🌟 ✨

If you do not wish to use pipx, you can install as follows.
```
python3 -m venv cpp  # create a virtual environment
source cpp/bin/activate  # activate the virtual environment
pip install -U pip  # upgrade pip
pip install create-python-package
```


Requires Python 3.6+.

## Example Session
```
> create-python-package /tmp/fake
Creating a new Python package in /private/tmp/fake

Creating a virtual environment at /private/tmp/fake/venv
Upgrading pip in the virtual environment.

Initialized a git repository.

Success! Created fake at /private/tmp/fake
Inside that directory, you can run several commands

  source activate
     Activates this package's isolated Python environment

  pip install PACKAGE
    Installs a package to current environment

  pip install -e .
    Installs this package in editable mode to the current environment

We suggest that you being by typing:

  cd fake
  source activate

To deactivate the virtual environment, type `deactivate`.

Questions? Create an issue at https://github.com/cs01/create-python-package

Happy hacking!
```

## Credits
Created and published using `create-python-package` 😄

Inspired by [create-react-app](https://github.com/facebook/create-react-app)
