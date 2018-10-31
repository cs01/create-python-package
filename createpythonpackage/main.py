#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path
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
    print("0.0.0.6")


class CppError(Exception):
    pass


def _run(cmd, check=True, **kwargs):
    cmd_str = " ".join(str(c) for c in cmd)
    logging.info(f"running {cmd_str}")
    returncode = subprocess.run(cmd, **kwargs).returncode
    if check and returncode:
        raise CppError(f"{cmd_str!r} failed with returncode {str(returncode)}")
    return returncode


def _create_venv(path: Path, name: str, python: str = sys.executable):
    venv = path / "venv"
    if venv.exists() and len(list(venv.iterdir())):
        raise CppError(
            f"Directory {str(venv)!r} already exists. Remove then try again."
        )
    print(f"Creating a virtual environment at {blue(str(venv))}")
    if _run([python, "-m", "venv", venv, "--prompt", name]):
        raise CppError("Could not create virtual environment")
    print(f"Upgrading {blue('pip')} in the virtual environment.")
    if _run([path / "venv/bin/pip", "install", "--upgrade", "--quiet", "pip"]):
        logging.warning("Could not upgrade pip to latest verions")
    print()
    return venv


def symlink_venv(path: Path):
    relative_path = (path / "venv/bin/activate").relative_to(path)
    try:
        (path / "activate").symlink_to(relative_path)
    except FileExistsError:
        logging.warning(f"File already exists at {str(relative_path)!r}")


class Package:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.add_files()
        _create_venv(self.path, self.name)
        symlink_venv(self.path)
        self.git_init()

    def git_init(self):
        _run(["git", "init", self.path], stdout=subprocess.DEVNULL)
        print("Initialized a git repository.")
        print()

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


def _create_package(args):
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


def _build_package(path):
    if (path / "dist").exists() and list((path / "dist").iterdir()):
        raise CppError(
            f"Remove {str(path/'dist')!r} directory before building "
            "to ensure a clean build"
        )
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
    printblue("Package has been built! See output in 'dist' directory.")


def _publish(path, test):
    cmd = ["python", "-m", "twine", "upload"]
    if test:
        cmd += ["--repository-url", TEST_PYPI_URL]
    cmd += ["dist/*"]
    printblue("Uploading package")
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    _run(cmd)


def create_package():
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
        package = _create_package(args)
        package.print_success()
        exit(0)
    except CppError as e:
        exit(e)


def build_package():
    parser = argparse.ArgumentParser(
        description="build a package but do not publish it"
    )
    parser.add_argument(
        "path", help="Path to root of package (setup.py should be in this dir)"
    )
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    _setup_logging(args.verbose)
    try:
        path = Path(args.path).resolve()
        if not path.is_dir():
            exit(f"Directory {args.path} does not exist")
        elif not (path / "setup.py").is_file():
            exit(f"{str(path / 'setup.py')} does not exist")
        _build_package(Path(args.path))
    except CppError as e:
        exit(e)


def create_venv():
    parser = argparse.ArgumentParser(
        description="create a virtual environment for the given directory"
    )
    parser.add_argument(
        "path",
        default=".",
        help="Path where venv should be created (usually the root of a package next to setup.py)",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python binary this venv should be associated with",
    )
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    _setup_logging(args.verbose)
    try:
        path = Path(args.path).resolve()
        mkdir(path)
        venv = _create_venv(path, path.name, args.python)
        symlink_venv(path)
        if (path / "requirements.txt").exists():
            logging.info("Installing from requirements.txt file")
            _run(
                [
                    venv / "bin" / "python",
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    path / "requirements.txt",
                ]
            )
        printblue("A new virtual environment has been created!")
        print()
        print(
            f"Run cd {str(path)!r} then type `source activate` "
            "to activate it. When you are finished type `deactivate` to exit the environment."
        )
    except CppError as e:
        exit(e)


def publish():
    parser = argparse.ArgumentParser(
        description="builds an publishes a package to PyPI"
    )
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
        _build_package(path)
        _publish(path, args.test)
    except CppError as e:
        exit(e)


if __name__ == "__main__":
    create_package()
