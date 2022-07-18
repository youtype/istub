import difflib
import logging
from abc import ABC, abstractmethod

from istub.constants import LOGGER_NAME
from istub.exceptions import CheckFailedError
from istub.package import Package
from istub.utils import cleanup_output


class BaseCheck(ABC):
    NAME = "base"

    def __init__(self, package: Package) -> None:
        self.package = package
        self.logger = logging.Logger(LOGGER_NAME)

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
        return list(difflib.ndiff(old_data, data))
