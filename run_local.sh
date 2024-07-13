#!/bin/bash
set -eu

# Venv doesn't need to be shellchecked
# shellcheck disable=SC1091
. ./venv/bin/activate
python -m src

cd ./out
python -m http.server
