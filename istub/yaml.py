from typing import Any

import yaml
from yaml.dumper import SafeDumper
from yaml.loader import SafeLoader
from yaml.nodes import Node, ScalarNode


class MyDumper(SafeDumper):
    """
    Custom YAML dumper that replaces system paths to avoid snapshot mismatch.
    """

    def represent_data(self, data: Any) -> Node:
        if isinstance(data, str):
            return self.represent_str(data)
        return super().represent_data(data)

    def represent_str(self, data: str) -> ScalarNode:
        if "\n" in data:
            return self.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return super().represent_str(data)


def dumps(data: Any) -> str:
    return yaml.dump(
        data,
        Dumper=MyDumper,
        indent=2,
    )


def loads(data: str) -> Any:
    return yaml.load(data, Loader=SafeLoader)
