#!/usr/bin/env python
"""
Main API entrypoint.
"""
import logging
import shlex
import sys

from istub.checks.base import BaseCheck
from istub.cli import parse_args
from istub.config import Config
from istub.constants import LOGGER_NAME
from istub.exceptions import CheckFailedError, ConfigError
from istub.logger import setup_logging
from istub.subprocess import check_call


def install(config: Config) -> None:
    """
    Install requirements.
    """
    logger = logging.Logger(LOGGER_NAME)
    if config.pip_uninstall:
        logger.info("Uninstalling pip packages...")
        check_call([sys.executable, "-m", "pip", "uninstall", *config.pip_uninstall])
    if config.pip_install:
        logger.info("Installing pip requirements...")
        check_call([sys.executable, "-m", "pip", "install", *config.pip_install])
    if config.path_install:
        logger.info("Installing requirements...")
        for path_package in config.path_install:
            logger.debug(f"  Installing {path_package.as_posix()}")
            check_call([sys.executable, "-m", "pip", "install", path_package.as_posix()])


def get_check_cls(name: str, checks: list[type[BaseCheck]]) -> type[BaseCheck]:
    """
    Get check class by name.
    """
    for check in checks:
        if check.NAME == name:
            return check
    raise ConfigError(f"Unknown check {name}")


def main() -> None:
    """
    Main API entrypoint.
    """
    args = parse_args()
    logger = setup_logging(args.log_level)
    config = args.config
    if args.packages:
        config.filter(args.packages)
    if args.build and config.build:
        logger.info("Building requirements...")
        for build_cmd in config.build:
            logger.debug(f"  Running {' '.join(build_cmd)}")
            check_call(shlex.split(build_cmd))
    if args.install:
        install(config)

    errors: list[BaseException] = []
    for package in config.packages:
        for check_name in package.enabled_checks:
            check = get_check_cls(check_name, args.checks)(package)
            logger.info(f"Checking {package.name} with {check.NAME}...")
            try:
                check.check()
            except CheckFailedError as e:
                if args.update:
                    package.set_snapshot(check.NAME, e.data)
                    continue

                logger.error(e)
                for line in e.diff:
                    logger.error(line)
                errors.append(e)

    if config.is_updated():
        config.save()

    if errors:
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except ConfigError as e:
        setup_logging(logging.INFO).error(f"Configuration error: {e}")
        exit(1)
