#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

# vulture istub --make-whitelist > vulture_whitelist.txt
vulture istub vulture_whitelist.txt

npx pyright istub
flake8 istub
black istub
isort istub
mypy istub
