"""
Check package with ruff.
"""

from istub.checks.base import BaseCheck


class RuffCheck(BaseCheck):
    """
    Check package with ruff.
    """

    NAME = "ruff"

    def run(self) -> str:
        """
        Run the ruff check on the package.
        """
        return self.get_call_output(
            [
                self.python_path,
                "-m",
                "ruff",
                "--ignore",
                "E203,E501,D200,D107,D401,D105,D205,D400,D101,D102,D403",
                self.package.path.as_posix(),
            ],
            capture_stderr=True,
        )
