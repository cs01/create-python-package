#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path
from .Package import Package, PackageConfig, PackageEnv, PackageLicense
from .util import blue, printblue, TEST_PYPI_URL, CppError, mkdir, run, grey
from typing import Optional, List

try:
    from bullet import Bullet
except ImportError:
    Bullet = None

__version__ = "0.3.0.0"


def print_version():
    print(__version__)


QUESTION_MARK = grey("[?]")


def question(s, default, options: Optional[List[str]] = None) -> str:
    while True:
        if options:
            response = list_question(s, default, options)
        else:
            response = input(f"{QUESTION_MARK} {s} ({default}): ")
        if not response:
            return default
        return response


def list_question(s, default, options: List[str]) -> str:
    if Bullet is not None:
        cli = Bullet(
            prompt=f"{QUESTION_MARK} {s} ({default}):", choices=options, margin=1
        )
        return cli.launch()

    # Fallback to a home-made list prompt.

    num_to_option = {str(i + 1): option for i, option in enumerate(options)}
    options_str = "\n".join([f"{i}) {option}" for i, option in num_to_option.items()])

    response = input(f"{QUESTION_MARK} {s} ({default}):\n{options_str}\n> ")
    response = num_to_option.get(response, response)

    return response


def _create_package(args):
    path = Path(args.name).resolve()
    if path.exists() and len(list(path.iterdir())) and not args.force:
        raise CppError(
            f"{str(path)} already exists and is not empty. Delete it then try again."
        )

    envs = [o.name for o in PackageEnv]
    licenses = [o.name for o in PackageLicense]

    default_version = "0.0.0.1"
    default_description = ""
    default_entrypoint = "main.py"
    default_repo_url = ""  # TODO get repo origin if in a git repo
    default_author = "Your Name"  # TODO get repo author if in a git repo
    default_email = "email@domain.com"  # TODO get repo email if in a git repo
    default_env = envs[0]
    default_license = licenses[0]

    if args.yes:
        package_config = PackageConfig(
            **{
                "path": path,
                "version": default_version,
                "description": default_description,
                "entrypoint": default_entrypoint,
                "repo_url": default_repo_url,
                "author": default_author,
                "email": default_email,
                "env": default_env,
                "userlicense": default_license,
                "force": args.force,
            }
        )
    else:
        package_config = PackageConfig(
            **{
                "path": path,
                "version": question("version", default_version),
                "description": question("description", default_description),
                "entrypoint": question("entry point", default_entrypoint),
                "repo_url": question("repository url", default_repo_url),
                "author": question("author", default_author),
                "email": question("email", default_email),
                "env": question("environment management", default_env, options=envs),
                "userlicense": question("license", default_license, options=licenses),
                "force": args.force,
            }
        )

    print(f"Creating a new Python package in {blue(str(path))}")
    print()
    mkdir(path)
    return Package(package_config)


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
    run(cmd)

    cmd = ["python", path / "setup.py", "--quiet", "sdist", "bdist_wheel"]
    printblue("Building package")
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    run(cmd)
    printblue("Package has been built! See output in 'dist' directory.")


def _publish(path, test):
    cmd = ["python", "-m", "twine", "upload"]
    if test:
        cmd += ["--repository-url", TEST_PYPI_URL]
    cmd += ["dist/*"]
    printblue("Uploading package")
    print(f"  {' '.join(list(str(c) for c in cmd))}")
    print()
    run(cmd)


def create_package():
    parser = argparse.ArgumentParser(
        description="Create the file and folder structure for a Python package",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    default_name = Path.cwd().name
    parser.add_argument(
        "name", nargs="?", default=default_name, help="Name of package to create"
    )
    parser.add_argument("--yes", action="store_true", help="Use default options")
    parser.add_argument(
        "--force",
        help="create package in existing directory (may delete or overwrite existin files!)",
        action="store_true",
    )
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.version:
        print_version()
        exit(0)

    _setup_logging(args.verbose)
    try:
        package = _create_package(args)
        package.print_success()
        exit(0)
    except CppError as e:
        exit(e)
    except KeyboardInterrupt:
        print()
        exit(1)


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
