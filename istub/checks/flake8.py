import sys

from istub.checks.base import BaseCheck
from istub.subprocess import get_call_output


class Flake8Check(BaseCheck):
    NAME = "flake8"

    def run(self) -> str:
        return get_call_output(
            [
                sys.executable,
                "-m",
                "flake8",
                "--ignore",
                "E203,W503,E501,D200,D107,D401,D105,D205,D400,D101,D102,D403",
                self.package.path.as_posix(),
            ],
            capture_stderr=True,
        )
