import json

from istub.checks.base import BaseCheck
from istub.subprocess import get_call_output


class PyrightCheck(BaseCheck):
    NAME = "pyright"

    def run(self) -> str:
        output = get_call_output(
            ["npx", "pyright", self.package.path.as_posix(), "--outputjson"],
            capture_stderr=False,
        )
        errors = json.loads(output).get("generalDiagnostics", [])

        if not errors:
            return ""

        messages = []
        for error in errors:
            messages.append(
                f'{error["file"]}:{error["range"]["start"]["line"]} {error.get("message", "")}'
            )
        return "\n".join(messages)
