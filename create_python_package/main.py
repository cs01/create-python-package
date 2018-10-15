#!/usr/bin/env python

import argparse
from pathlib import Path
import logging
import shutil
import subprocess
from create_python_package import templates

TEST_PYPI_URL = "https://test.pypi.org/simple/"


def print_version():
    print("0.0.0.3")


class CppError(Exception):
    pass


def _run(cmd, check=True):
    cmd_str = " ".join(str(c) for c in cmd)
    logging.info(f"running {cmd_str}")
    returncode = subprocess.run(cmd).returncode
    if check and returncode:
        raise CppError(f"{cmd_str!r} failed with returncode {str(returncode)}")
    return returncode


class Package:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.add_files()
        self.create_venv()
        self.symlink_venv()

    def create_venv(self):
        _run(["python3", "-m", "venv", self.path / "venv", "--prompt", self.name])
        _run([self.path / "venv/bin/pip", "install", "--upgrade", "--quiet", "pip"])

    def symlink_venv(self):
        (self.path / "activate-venv").symlink_to(self.path / "venv/bin/activate")

    def add_files(self):
        (self.path / self.name).mkdir(exist_ok=True)
        (self.path / self.name / "__init__.py").touch()

        with open(self.path / "README.md", "w") as f:
            f.write(templates.readme % self.name)

        with open(self.path / "setup.py", "w") as f:
            f.write(templates.setup % self.name)

        with open(self.path / self.name / "main.py", "w") as f:
            f.write(templates.main)

        with open(self.path / ".gitignore", "w") as f:
            f.write(templates.gitignore)

        with open(self.path / "LICENSE", "w") as f:
            f.write(templates.licence)

    def print_success(self):
        print(f"Created package in {self.path}.")
        print(
            f"To activate package's virtualenv, cd to {self.path} "
            "then run `source activate-venv`. To deactivate, type `deactivate`."
        )
        print(
            "Questions? Create an issue at https://github.com/cs01/create-python-package"
        )


def mkdir(path):
    if path.is_dir():
        return
    logging.info(f"creating directory {path}")
    path.mkdir(parents=True, exist_ok=True)


def _create(args):
    name = Path(args.name).name
    path = Path(args.name).resolve()
    if Path(args.name).exists() and len(list(path.iterdir())):
        raise CppError(f"{str(path)} already exists and is not empty")
    mkdir(path)
    return Package(path, name)


def _setup_logging(verbose):
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="create-python-package (%(funcName)s:%(lineno)d): %(message)s",
        )
    else:
        logging.basicConfig(level=logging.WARNING, format="%(message)s")


def create():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", help="Name of package to create")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print_version()
        exit(0)
    if not args.name:
        exit("path is required")

    _setup_logging(args.verbose)

    try:
        package = _create(args)
        package.print_success()
        exit(0)
    except CppError as e:
        exit(e)


def _publish(path, test):
    print(
        "running instructions from https://packaging.python.org/tutorials/packaging-projects/"
    )
    _run(["pip", "install", "--upgrade", "setuptools", "wheel", "twine"])
    _run(["python", path / "setup.py", "sdist", "bdist_wheel"])
    upload_cmd = ["python", "-m", "twine", "upload"]
    if test:
        upload_cmd += ["--repository-url", TEST_PYPI_URL]
    upload_cmd += ["dist/*"]
    _run(upload_cmd)


def publish():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to root of package (setup.py should be in this dir)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help=f"publish to {TEST_PYPI_URL} instead of the real PyPI",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print_version()
        exit(0)
    if not args.path:
        exit("path is required")

    _setup_logging(args.verbose)

    try:
        path = Path(args.path).resolve()
        if not path.is_dir():
            exit(f"Directory {args.path} does not exist")
        elif not (path / "setup.py").is_file():
            exit(f"{str(path / 'setup.py')} does not exist")
        _publish(path, args.test)
        exit(0)
    except CppError as e:
        exit(e)


if __name__ == "__main__":
    create()
