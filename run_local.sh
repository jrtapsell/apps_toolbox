#!/bin/bash
set -eu

. ./venv/bin/activate
python -m src

cd ./out
python -m http.server
