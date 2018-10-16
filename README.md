# create-python-package
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/). Perfect for beginners and experts alike. No more guesswork!


## Quick Overview
```
create-python-package mypackage
cd mypackage
source activate-venv
```

And to publish, run
```
publish-python-package mypackage
```

## Virtualenv ready to go!
Inside the directory you can run
```
source activate-venv
```
to activate an isolated Python environment that was created specifically for that package. To deactivate it, type
```
deactivate
```

To learn more about virtual environments, see [Creating Virtual Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments).

## Usage and Installation
*[pipx](https://github.com/cs01/pipx) allows you to run or install Python binaries from packages*

To run the latest version

```
> pipx create-python-package mypackage  # directly runs latest version
```

and to publish
```
> pipx --package create-python-package publish-python-package mypackage  # directly runs latest version
```

If you would rather install to your system and freeze the version
```
> pipx install create-python-package
```
To upgrade the installation
```
> pipx upgrade create-python-package
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

  source activate-venv
     Activates this package's isolated Python environment

  pip install PACKAGE
    Installs a package to current environment

  pip install -e .
    Installs this package in editable mode to the current environment

We suggest that you being by typing:

  cd fake
  source activate-venv fake

To deactivate the virtual environment, type `deactivate`.

Questions? Create an issue at https://github.com/cs01/create-python-package

Happy hacking!
```

## Credits
Created and published using `create-python-package` 😄

Inspired by [create-react-app](https://github.com/facebook/create-react-app)
