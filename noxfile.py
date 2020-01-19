import nox  # type: ignore
from pathlib import Path

lint_dependencies = ["black", "flake8", "flake8-bugbear", "mypy", "check-manifest"]


@nox.session(python="3.7")
def lint(session):
    session.install(*lint_dependencies)
    files = ["createpythonpackage"] + [str(p) for p in Path(".").glob("*.py")]
    session.run("black", "--check", *files)
    session.run("flake8", *files)
    session.run("mypy", *files)
    session.run("check-manifest")
    session.run("python", "setup.py", "check", "--metadata", "--strict")


@nox.session(python="3.7")
def build(session):
    session.install("setuptools")
    session.install("wheel")
    session.install("twine")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


@nox.session(python="3.7")
def publish(session):
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
