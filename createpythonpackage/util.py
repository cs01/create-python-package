import logging
import os
import subprocess
import sys

TEST_PYPI_URL = "https://test.pypi.org/simple/"
ISATTY = sys.stdout.isatty()
WINDOWS = os.name == "nt"


class CppError(Exception):
    pass


def blue(text):
    if ISATTY and not WINDOWS:
        return "\033[1;34m" + text + "\033[0m"
    return text


def grey(text):
    if ISATTY and not WINDOWS:
        # return "\033[1;34m" + text + "\033[0m"
        return "\033[1;30m" + text + "\033[0m"
    return text


def printblue(text):
    print(blue(text))


def run(cmd, check=True, **kwargs):
    cmd_str = " ".join(str(c) for c in cmd)
    logging.info(f"running {cmd_str}")
    returncode = subprocess.run(cmd, **kwargs).returncode
    if check and returncode:
        raise CppError(f"{cmd_str!r} failed with returncode {str(returncode)}")
    return returncode


def mkdir(path):
    if path.is_dir():
        return
    logging.info(f"creating directory {path}")
    path.mkdir(parents=True, exist_ok=True)
