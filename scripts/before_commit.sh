#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

# uvx vulture src/istub --make-whitelist > vulture_whitelist.txt
uvx pre-commit run --all-files

# uv run pytest --cov-report html --cov src/istub
