#!/usr/bin/env bash
set -euo pipefail

cd app/blog-platform
python -m pip install -e ".[linting]"
flake8 --exclude=setup.py --count .
