"""
Base class for all checks.
"""

import difflib
import logging
from abc import ABC, abstractmethod
from typing import Iterable, List, Sequence, Tuple

from istub.constants import LOGGER_NAME
from istub.exceptions import CheckFailedError
from istub.package import CheckConfig, Package
from istub.subprocess import get_call_output
from istub.utils import cleanup_output, get_python_path_str


class BaseCheck(ABC):
    """
    Base class for all checks.
    """

    NAME = "base"

    def __init__(self, package: Package) -> None:
        self.package = package
        self.logger = logging.getLogger(LOGGER_NAME)

    @property
    def config(self) -> CheckConfig:
        """
        Check config.
        """
        return self.package.get_check_config(self.NAME)

    @property
    def default_command(self) -> Tuple[str, ...]:
        """
        Default command to run the check.
        """
        return ()

    @property
    def command(self) -> Tuple[str, ...]:
        """
        Command to run the check.
        """
        if self.config.command:
            return tuple(self.config.command)

        return self.default_command

    def check(self) -> None:
        """
        Run the check and raise an exception if it fails.
        """
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
        """
        Run the check and return its output.
        """

    def get_diff(self, data: List[str]) -> List[str]:
        """
        Compare tool output with a snapshot.
        """
        old_data = self.package.get_snapshot(self.NAME)
        if data == old_data:
            return []

        differ = difflib.Differ()
        diff = differ.compare(old_data, data)
        return [i for i in diff if not self.is_ignored_line_diff(i)]

    def get_call_output(
        self,
        cmd: Sequence[str],
        capture_stderr: bool = False,
        raise_errors: bool = False,
    ) -> str:
        """
        Run a command and return its output.
        """
        self.logger.debug(" ".join(cmd))
        return get_call_output(cmd, capture_stderr, raise_errors)

    @property
    def python_path(self) -> str:
        """
        Python executable path.
        """
        return get_python_path_str()

    def set_snapshot(self, data: Iterable[str]) -> None:
        """
        Set snapshot data.
        """
        self.package.set_snapshot(self.NAME, data)

    def is_ignored_line_diff(self, line: str) -> bool:
        """
        Whether line is ignored in diff.
        """
        if line.startswith("+") or line.startswith("-"):
            return False
        return True
