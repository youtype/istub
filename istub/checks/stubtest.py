import sys

from istub.checks.base import BaseCheck
from istub.subprocess import get_call_output


class StubtestCheck(BaseCheck):
    NAME = "stubtest"

    def run(self) -> str:
        return get_call_output(
            [sys.executable, "-m", "mypy.stubtest", self.package.name],
            capture_stderr=True,
        )
