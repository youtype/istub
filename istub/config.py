"""
iStub config.
"""
import itertools
from pathlib import Path
from typing import Any, Iterable, Iterator, TypeVar

from istub.checks import CHECKS_MAP
from istub.checks.base import BaseCheck
from istub.exceptions import ConfigError
from istub.package import Package
from istub.utils import get_python_path_str
from istub.yaml import dumps, loads

_V = TypeVar("_V")


class Config:
    """
    iStub config.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.enabled_check_names: list[str] = list(CHECKS_MAP)
        try:
            self.data = loads(path.read_text())
        except Exception as e:
            raise ConfigError(f"Cannot read config: {e}")
        try:
            self._packages = [Package.deserialize(self.path, i) for i in self.data["packages"]]
        except ValueError as e:
            raise ConfigError(e)
        self._map = {i.name: i for i in self._packages}
        self.packages = list(self._packages)

    def _uniq_lists(self, lists: Iterable[list[_V]]) -> list[_V]:
        result = []
        for item in itertools.chain.from_iterable(lists):
            if item not in result:
                result.append(item)
        return result

    @property
    def pip_install(self) -> list[str]:
        """
        List of pip install packages.
        """
        return self._uniq_lists([i.pip_install for i in self.packages])

    @property
    def pip_uninstall(self) -> list[str]:
        """
        List of pip uninstall packages.
        """
        return self._uniq_lists([i.pip_uninstall for i in self.packages])

    @property
    def path_install(self) -> list[Path]:
        """
        List of paths to install with pip.
        """
        return self._uniq_lists([i.path_install for i in self.packages])

    @property
    def build(self) -> list[str]:
        """
        List of commands to build packages.
        """
        return self._uniq_lists([i.build for i in self.packages])

    def get(self, name: str) -> Package:
        """
        Get package by name.
        """
        if name not in self._map:
            raise ConfigError(f"Package {name} not found")
        return self._map[name]

    def filter_packages(self, names: Iterable[str]) -> None:
        """
        Filter packages by names.
        """
        self.packages = [self.get(i) for i in names]

    def filter_checks(self, names: Iterable[str]) -> None:
        """
        Filter packages by names.
        """
        self.enabled_check_names = list(names)

    def serialize(self) -> dict[str, Any]:
        """
        Serialize config to dict.
        """
        return {
            "packages": [i.serialize() for i in self._packages],
        }

    def is_updated(self) -> bool:
        """
        Check if any of the packages are updated.
        """
        return any(i.updated for i in self.packages)

    def save(self) -> None:
        """
        Save config to file.
        """
        self.path.write_text(dumps(self.serialize()))

    def iterate_package_checks(self) -> Iterator[BaseCheck]:
        for package in self.packages:
            for check_name in package.enabled_checks:
                if check_name not in self.enabled_check_names:
                    continue

                yield CHECKS_MAP[check_name](package)

    @property
    def python_path(self) -> str:
        """
        Python executable path.
        """
        return get_python_path_str()
