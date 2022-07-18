"""
Stubs package data.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, TypeVar

_R = TypeVar("_R", bound="Package")


@dataclass
class Package:
    """
    Stubs package data.
    """

    name: str
    path: Path
    checks: dict[str, bool] = field(default_factory=dict)
    path_install: list[Path] = field(default_factory=list)
    pip_install: list[str] = field(default_factory=list)
    pip_uninstall: list[str] = field(default_factory=list)
    build: list[str] = field(default_factory=list)
    snapshots: dict[str, str] = field(default_factory=dict)
    updated: bool = False

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def deserialize(cls: type[_R], data: dict[str, Any]) -> _R:
        """
        Load package from config data.
        """
        name = data["name"]
        return cls(
            name=name,
            path=Path(data["path"]) if "path" in data else Path(f"./{name}-stubs"),
            checks=data.get("checks", {}),
            path_install=[Path(i) for i in data.get("install", [])],
            pip_install=data.get("pip_install", []),
            pip_uninstall=data.get("pip_uninstall", []),
            build=data.get("build", []),
            snapshots=data.get("snapshots", {}),
        )

    @property
    def enabled_checks(self) -> Iterator[str]:
        """
        Iterate over enabled checks in order.
        """
        for check in self.checks:
            if self.checks[check]:
                yield check

    def serialize(self) -> dict[str, Any]:
        """
        Serialize package to config data.
        """
        data = {
            "name": self.name,
            "checks": self.checks,
            "install": [i.as_posix() for i in self.path_install],
            "pip_install": self.pip_install,
            "pip_uninstall": self.pip_uninstall,
            "build": self.build,
            "snapshots": self.snapshots,
        }
        for key in list(data):
            if not data[key]:
                del data[key]
        return data

    def get_snapshot(self, name: str) -> list[str]:
        """
        Get snapshot data by check name.
        """
        return self.snapshots.get(name, "").strip().splitlines()

    def set_snapshot(self, name: str, data: list[str]) -> None:
        """
        Set snapshot data by check name.
        """
        if not data:
            if name in self.snapshots:
                del self.snapshots[name]
            return
        self.snapshots[name] = "\n".join(data).strip()
        self.updated = True
