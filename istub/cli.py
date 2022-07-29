"""
CLI parser.
"""
import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

from istub.checks import CHECKS_MAP
from istub.config import Config


@dataclass
class CLINamespace:
    """
    CLI namespace.
    """

    build: bool
    install: bool
    update: bool
    exitfirst: bool
    log_level: int
    config: Config
    packages: List[str]
    checks: List[str]


def load_config(path_str: str) -> Config:
    """
    Load config.
    """
    path = Path(path_str)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Config file {path.as_posix()} does not exist")
    return Config(path)


def parse_args() -> CLINamespace:
    """
    CLI parser.
    """
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument("-b", "--build", action="store_true", help="Generate packages")
    parser.add_argument("-i", "--install", action="store_true", help="Install packages")
    parser.add_argument("-u", "--update", action="store_true", help="Update snapshots")
    parser.add_argument(
        "-x", "--exitfirst", action="store_true", help="Exit on first check failure"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=load_config,
        default=None,
        help="Path to configuration file",
    )
    parser.add_argument(
        "--checks",
        nargs="*",
        default=[],
        choices=list(CHECKS_MAP),
        help="Checks to run",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Verbose output")
    parser.add_argument(
        "packages",
        nargs="*",
        help="Packages to check",
    )
    args = parser.parse_args()
    return CLINamespace(
        config=args.config or Config(Path.cwd() / "istub.yml"),
        build=args.build,
        install=args.install,
        update=args.update,
        exitfirst=args.exitfirst,
        packages=args.packages,
        log_level=logging.DEBUG if args.debug else logging.INFO,
        checks=args.checks,
    )
