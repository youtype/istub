#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

# poetry run vulture istub --make-whitelist > vulture_whitelist.txt
poetry run vulture istub vulture_whitelist.txt

poetry run npx pyright istub
poetry run flake8 istub
poetry run black istub
poetry run isort istub
poetry run mypy istub
