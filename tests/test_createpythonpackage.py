#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import tempfile
import subprocess
from pathlib import Path
from typing import Dict
from createpythonpackage.Package import (
    PackageConfig,
    Package,
    PackageEnv,
    PackageLicense,
)


class StaticTests(unittest.TestCase):
    def run_cmd(self, cmd):
        print(f"Running {' '.join(cmd)!r}")
        rc = subprocess.run(cmd).returncode
        if rc:
            print(f"test failed; exiting with code {rc}")
            exit(rc)

    def test_static(self):
        files = ["createpythonpackage", "tests"]
        self.run_cmd(["black", "--check"] + files)
        self.run_cmd(["flake8"] + files)
        self.run_cmd(["mypy"] + files)


class UnitTests(unittest.TestCase):
    def test_defaults(self):
        with tempfile.TemporaryDirectory(prefix="cpp_tests_") as t:
            subprocess.run(
                ["create-python-package", "--yes", str(Path(t) / "testpackage")],
                check=True,
            )

    def run_package(self, config: Dict):
        with tempfile.TemporaryDirectory(prefix="cpp_tests_") as t:
            config["path"] = Path(t)
            Package(PackageConfig(**config))

    def test_configs(self):
        path = None
        envs = [o.name for o in PackageEnv]
        licenses = [o.name for o in PackageLicense]

        default_version = "0.0.0.1"
        default_description = ""
        default_entrypoint = "main.py"
        default_repo_url = ""  # TODO get repo origin if in a git repo
        default_author = "Your Name"  # TODO get repo author if in a git repo
        default_email = "email@doman.com"  # TODO get repo email if in a git repo
        default_env = envs[0]
        default_license = licenses[0]

        print()
        for env in envs:
            print("testing env", env)
            self.run_package(
                {
                    "path": path,
                    "version": default_version,
                    "description": default_description,
                    "entrypoint": default_entrypoint,
                    "repo_url": default_repo_url,
                    "author": default_author,
                    "email": default_email,
                    "env": env,
                    "userlicense": default_license,
                    "force": True,
                }
            )

        print()
        for lic in licenses:
            print("testing license", lic)
            self.run_package(
                {
                    "path": path,
                    "version": default_version,
                    "description": default_description,
                    "entrypoint": default_entrypoint,
                    "repo_url": default_repo_url,
                    "author": default_author,
                    "email": default_email,
                    "env": default_env,
                    "userlicense": lic,
                    "force": True,
                }
            )


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(StaticTests, UnitTests))

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)

    num_failures = len(result.errors) + len(result.failures)
    return num_failures


if __name__ == "__main__":
    exit(main())
