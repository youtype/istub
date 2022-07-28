import sys

from istub.checks.base import BaseCheck
from istub.exceptions import SubprocessError


class MypyCheck(BaseCheck):
    NAME = "mypy"

    def run(self) -> str:
        try:
            self.get_call_output(
                [sys.executable, "-m", "mypy", self.package.path.as_posix(), "--exclude", "build"],
                capture_stderr=False,
                raise_errors=True,
            )
        except SubprocessError as e:
            return "\n".join(e.data.splitlines()[:-1])

        return ""
