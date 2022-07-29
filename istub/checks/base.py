import difflib
import logging
import shlex
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from istub.constants import LOGGER_NAME
from istub.exceptions import CheckFailedError
from istub.package import Package
from istub.subprocess import get_call_output
from istub.utils import cleanup_output, shorten_path


class BaseCheck(ABC):
    NAME = "base"

    def __init__(self, package: Package) -> None:
        self.package = package
        self.logger = logging.getLogger(LOGGER_NAME)

    def check(self) -> None:
        output = self.run()
        output_lines = cleanup_output(output.splitlines())
        diff = self.get_diff(output_lines)
        if not diff:
            return

        raise CheckFailedError(
            f"Check {self.NAME} failed for {self.package.name}",
            diff,
            output_lines,
        )

    @abstractmethod
    def run(self) -> str:
        pass

    def get_diff(self, data: list[str]) -> list[str]:
        """
        Compare tool output with a snapshot.
        """
        old_data = self.package.get_snapshot(self.NAME)
        if data == old_data:
            return []

        differ = difflib.Differ()
        diff = differ.compare(old_data, data)
        return [i for i in diff if i.startswith("-") or i.startswith("+")]

    def get_call_output(
        self,
        cmd: list[str],
        capture_stderr: bool = False,
        raise_errors: bool = False,
    ) -> str:
        """
        Run a command and return its output.
        """
        self.logger.debug(shlex.join(cmd))
        return get_call_output(cmd, capture_stderr, raise_errors)

    @property
    def python_path(self) -> str:
        """
        Python executable path.
        """
        return shorten_path(Path(sys.executable))

    def set_snapshot(self, data: list[str]) -> None:
        """
        Set snapshot data.
        """
        self.package.set_snapshot(self.NAME, data)
