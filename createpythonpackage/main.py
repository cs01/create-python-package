#!/usr/bin/env python3

import argparse
from cookiecutter.main import cookiecutter  # type: ignore
from click.exceptions import Abort

__version__ = "0.5.0.0"


def main():
    parser = argparse.ArgumentParser(
        description="Create the file and folder structure for a Python package",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--template",
        default="https://github.com/cs01/cookiecutter-pypackage",
        help="Template name or url.",
    )
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)

    print(f"Using template {args.template}")

    try:
        cookiecutter("cookiecutter-pypackage/")
    except Abort:
        print()
        exit(1)


if __name__ == "__main__":
    main()
