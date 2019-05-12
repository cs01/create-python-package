# `create-python-package` Changelog

Unreleased
* Add test framework option, with support for `unittest` and `pytest` (@florimondmanca)

0.3.0.0
* Change default environment manager to none

0.2.2.0
* Run `pipenv install -e .` instead of `pipenv install` when pipenv is chosen
* Add `python -m twine check` to generated makefile. Now `make publish` will also run `twine check`
* Allow ctrl+c (abort) to work when selecting from list choices by upgrading bullet library
* Add "none" license choice

0.2.1.0
* Run `pipenv install` if pipenv option was chosen (#2)
* Add 'none' option for environment management
* Update boilerplate for generated test
* Add `MANIFEST.in`

0.2.0.3
* [bugfix] Do not create venv twice (@florimondmanca)

0.2.0.2
* update text printed when using pipenv

0.2.0.0
* Remove all entrypoints but `create-python-package`
* Add interactive choices to command line
* Support multiple licenses
* Support venv, Pipenv, and poetry

0.1.0.0
* add makefile
* add more options to `create-python-package` (i.e. author, email)
* remove `activate` symlink
* show default options in help text
* add changelog
