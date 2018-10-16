#!/usr/bin/env python

import argparse
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
from createpythonpackage import templates

TEST_PYPI_URL = "https://test.pypi.org/simple/"
ISATTY = sys.stdout.isatty()
WINDOWS = os.name == "nt"


def blue(text):
    if ISATTY and not WINDOWS:
        return "\033[1;34m" + text + "\033[0m"
    return text


def printblue(text):
    print(blue(text))


def print_version():
    print("0.0.0.5")


class CppError(Exception):
    pass


def _run(cmd, check=True, **kwargs):
    cmd_str = " ".join(str(c) for c in cmd)
    logging.info(f"running {cmd_str}")
    returncode = subprocess.run(cmd, **kwargs).returncode
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
        self.git_init()

    def git_init(self):
        _run(["git", "init", self.path], stdout=subprocess.DEVNULL)
        print("Initialized a git repository.")
        print()

    def create_venv(self):
        venv = self.path / "venv"
        print(f"Creating a virtual environment at {blue(str(venv))}")
        _run(["python3", "-m", "venv", venv, "--prompt", self.name])
        _run([self.path / "venv/bin/pip", "install", "--upgrade", "--quiet", "pip"])
        print(f"Upgrading {blue('pip')} in the virtual environment.")
        print()

    def symlink_venv(self):
        relative_path = (self.path / "venv/bin/activate").relative_to(self.path)
        (self.path / "activate-venv").symlink_to(relative_path)

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
        print(f"Success! Created {self.name} at {str(self.path)}")
        print("Inside that directory, you can run several commands")
        print()
        printblue("  source activate-venv")
        print("     Activates this package's isolated Python environment")
        print()
        printblue("  pip install PACKAGE")
        print("    Installs a package to current environment")
        print()
        printblue("  pip install -e .")
        print("    Installs this package in editable mode to the current environment")
        print()
        print(
            f"We suggest that you being by typing:\n\n"
            f"  {blue('cd')} {self.name}\n"
            f"  {blue('source activate-venv')}\n\n"
            "To deactivate the virtual environment, type `deactivate`.\n"
        )
        print(
            "Questions? Create an issue at https://github.com/cs01/create-python-package"
        )
        print()
        print("Happy hacking!")


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
    print(f"Creating a new Python package in {blue(str(path))}")
    print()
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
    if (path / "dist").exists() and list((path / "dist").iterdir()):
        raise CppError(f"Remove {str(path/'dist')} before publishing")
    print(
        "running instructions from https://packaging.python.org/tutorials/packaging-projects/"
    )
    print(f"Upgrading {blue('setuptools')}, {blue('wheel')}, and {blue('twine')}")
    cmd = ["pip", "install", "--upgrade", "--quiet", "setuptools", "wheel", "twine"]
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    _run(cmd)


    cmd = ["python", path / "setup.py", "--quiet", "sdist", "bdist_wheel"]
    printblue("Building package")
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    _run(cmd)

    cmd = ["python", "-m", "twine", "upload"]
    if test:
        cmd += ["--repository-url", TEST_PYPI_URL]
    cmd += ["dist/*"]
    printblue("Uploading package")
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    _run(cmd)


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
