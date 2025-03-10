"""
Check package with pyright.
"""

import json
from typing import Tuple

from istub.checks.base import BaseCheck


class PyrightCheck(BaseCheck):
    """
    Check package with pyright.
    """

    NAME = "pyright"

    @property
    def default_command(self) -> Tuple[str, ...]:
        """
        Default command to run the check.
        """
        return ("pyright",)

    def run(self) -> str:
        """
        Run the Pyright check on the package.
        """
        command = [*self.command, self.package.path.as_posix(), "--outputjson"]
        output = self.get_call_output(command, capture_stderr=False)
        try:
            errors = json.loads(output).get("generalDiagnostics", [])
        except json.JSONDecodeError:
            return self.get_call_output(command, capture_stderr=True)

        if not errors:
            return ""

        messages = []
        for error in errors:
            messages.append(
                f"{error['file']}:{error['range']['start']['line']} {error.get('message', '')}"
            )
        return "\n".join(messages)
