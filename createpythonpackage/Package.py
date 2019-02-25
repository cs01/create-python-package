#!/usr/bin/env python3

from .util import run, printblue, blue, mkdir
import subprocess
from . import templatestrs
from .createvenv import create_venv
from jinja2 import Template
import pkgutil
from pathlib import Path
from typing import NamedTuple
import datetime
import enum
import logging


class PackageEnv(enum.Enum):
    venv = enum.auto()
    pipenv = enum.auto()
    poetry = enum.auto()


class PackageLicense(enum.Enum):
    mit = enum.auto()
    gplv3 = enum.auto()
    apache2 = enum.auto()
    bsd3 = enum.auto()


def _get_template(name: str) -> Template:
    data = pkgutil.get_data("createpythonpackage", f"templates/{name}")
    if not data:
        raise ValueError(f"Developer error: expected to find template {name}")

    return Template(data.decode("utf-8"))


class PackageConfig(NamedTuple):
    path: Path
    version: str
    description: str
    entrypoint: str
    repo_url: str
    author: str
    email: str
    env: str
    userlicense: str
    force: bool


class Package:
    def __init__(self, config: PackageConfig):
        self.config = config
        self.path = config.path
        self.name = config.path.name
        self.version = config.version
        self.description = config.description
        self.entrypoint = config.entrypoint
        self.repo_url = config.repo_url
        self.author = config.author
        self.email = config.email
        self.env = config.env
        self.userlicense = config.userlicense
        self.force = config.force

        self.write_files()
        self.init_env()
        self.git_init()

    @property
    def license_classifier(self):
        if self.userlicense.lower() == PackageLicense.mit.name.lower():
            return "License :: OSI Approved :: MIT License"
        elif self.userlicense.lower() == PackageLicense.gplv3.name.lower():
            return "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        elif self.userlicense.lower() == PackageLicense.apache2.name.lower():
            return "License :: OSI Approved :: Apache Software License"
        elif self.userlicense.lower() == PackageLicense.bsd3.name.lower():
            return "License :: OSI Approved :: BSD License"
        else:
            return f"License :: {self.userlicense} License"

    def init_env(self):
        if self.env.lower() == PackageEnv.venv.name.lower():
            create_venv(self.path, self.name, force=self.force)
        elif self.env.lower() == PackageEnv.pipenv.name.lower():
            Path(self.path / "Pipfile").touch()
        elif self.env.lower() == PackageEnv.poetry.name.lower():
            logging.warning(
                "poetry has its own package initialization script. "
                "Use it instead of create-python-package."
            )
        else:
            print(self.env.lower(), "vs", PackageEnv.venv.name.lower())
            print(f"unknown env option {self.env}")

    def git_init(self):
        run(["git", "init", self.path], stdout=subprocess.DEVNULL)
        print("Initialized a git repository.")
        print()

    def write_files(self):
        (self.path / self.name).mkdir(exist_ok=True)
        (self.path / self.name / "__init__.py").touch()

        with open(self.path / "README.md", "w") as f:
            f.write(
                templatestrs.readme.format(name=self.name, description=self.description)
            )

        with open(self.path / "setup.py", "w") as f:
            entry_filename = self.entrypoint.replace(".py", "")
            f.write(
                _get_template("setup.py").render(
                    license=self.userlicense,
                    repo_url=self.repo_url,
                    name=self.name,
                    author=self.author,
                    email=self.email,
                    entry_point=f"{self.name}={self.name}.{entry_filename}:main",
                    license_classifier=self.license_classifier,
                )
            )

        with open(self.path / self.name / self.entrypoint, "w") as f:
            f.write(_get_template("entrypoint.py").render(version=self.version))

        with open(self.path / ".gitignore", "w") as f:
            f.write(templatestrs.gitignore)

        self.add_license()

        with open(self.path / "makefile", "w") as f:
            f.write(_get_template("makefile").render())

        mkdir(self.path / "tests")
        with open(self.path / "tests" / "test_project.py", "w") as f:
            f.write(
                _get_template("test_project.py").render(
                    license=self.userlicense,
                    repo_url=self.repo_url,
                    name=self.name,
                    author=self.author,
                    email=self.email,
                    entry_point=f"{self.name}={self.name}.{entry_filename}:main",
                )
            )

    def add_license(self):
        year = datetime.datetime.now().year
        with open(self.path / "LICENSE", "w") as f:
            if self.userlicense.lower() == PackageLicense.mit.name.lower():
                f.write(_get_template("mit_license.txt").render(author=self.author))
            elif self.userlicense.lower() == PackageLicense.gplv3.name.lower():
                f.write(_get_template("gplv3_license.txt").render(author=self.author))
            elif self.userlicense.lower() == PackageLicense.apache2.name.lower():
                f.write(
                    _get_template("apache2_license.txt").render(
                        author=self.author, year=year
                    )
                )
            elif self.userlicense.lower() == PackageLicense.bsd3.name.lower():
                f.write(
                    _get_template("bsd3_license.txt").render(
                        author=self.author, year=year
                    )
                )
            else:
                f.write(f"{self.userlicense} License\n\nCopyright (c) {self.author}")

    def print_success(self):
        print(f"Success! Created {self.name} at {str(self.path)}")
        print("Inside that directory, you can run several commands")
        print()
        print("  python setup.py tests  # runs unit tests")
        print
        print("  make publish  # builds and publishes to PyPI")
        print()
        if self.env.lower() == PackageEnv.venv.name.lower():
            printblue("  source ven/bin/activate")
            print("     Activates this package's isolated Python environment")
            print()
            printblue("  pip install PACKAGE")
            print("    Installs a package to current environment")
            print()
            printblue("  pip install -e .")
            print(
                "    Installs this package in editable mode to the current environment"
            )
            print()
            print(
                f"We suggest that you being by typing:\n\n"
                f"  {blue('cd')} {self.name}\n"
                f"  {blue('source ven/bin/activate')}\n\n"
                "To deactivate the virtual environment, type `deactivate`.\n"
            )
            create_venv(self.path, self.name, force=self.force)
        elif self.env.lower() == PackageEnv.pipenv.name.lower():
            print("  pipenv -e .")
            print()
        print(
            "Questions? Create an issue at https://github.com/cs01/create-python-package"
        )
        print()
        print("Happy hacking!")
