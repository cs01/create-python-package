# create-python-package
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/).

Perfect for beginners and experts alike!

```
> create-python-package mypackage
```

No more guesswork!

The file structure you're left with looks like this
```
mypackage/
├── LICENSE
├── README.md
├── activate-venv -> /private/tmp/mypackage/venv/bin/activate
├── mypackage
│   ├── __init__.py
│   └── main.py
└── setup.py
```

To publish, run
```
> publish-python-package packagepath
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

## Install
Install [pipx](https://github.com/cs01/pipx), then use `pipx` to install `create-python-package`.
```
> pipx install create-python-package
```

You can also run the latest version of `create-python-package` with
```
> pipx create-python-package mypackage  # runs latest version
```

and to publish
```
> pipx --package create-python-package publish-python-package mypackage  # runs latest version
```

Requires Python 3.6+.

## Credits
Inspired by [create-react-app](https://github.com/facebook/create-react-app)
