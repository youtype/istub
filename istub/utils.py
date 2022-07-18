import re
import sys
from functools import cache
from pathlib import Path

HASH_RE = re.compile(r"0x[0-9a-f]{12}")


@cache
def get_replace_paths() -> list[str]:
    """
    Generate a list of paths to replace in snapshot.
    """
    root_path = f"{Path.cwd()}/"
    result = [*sys.path, *[i.replace(root_path, "") for i in sys.path]]
    result = list(filter(lambda x: "/" in x, result))
    result.sort(key=lambda x: len(x), reverse=True)
    return result


def cleanup_output(data: list[str]) -> list[str]:
    result = []
    for line in data:
        line = HASH_RE.sub("HASH", line)
        for path in get_replace_paths():
            line = line.replace(path, ".")
        result.append(line)
    while result and not result[0]:
        result = result[1:]
    while result and not result[-1]:
        result.pop()
    return result
