import sys
import logging
from .util import CppError, run, blue
from pathlib import Path


def create_venv(path: Path, name: str, *, force: bool, python: str = sys.executable):
    venv = path / "venv"
    if venv.exists() and len(list(venv.iterdir())) and not force:
        raise CppError(
            f"Directory {str(venv)!r} already exists. Remove then try again."
        )
    print(f"Creating a virtual environment at {blue(str(venv))}")
    if run([python, "-m", "venv", venv, "--prompt", name]):
        raise CppError("Could not create virtual environment")
    print(f"Upgrading {blue('pip')} in the virtual environment.")
    if run([path / "venv/bin/pip", "install", "--upgrade", "--quiet", "pip"]):
        logging.warning("Could not upgrade pip to latest verions")
    print()
    return venv
