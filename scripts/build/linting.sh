#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e ".[linting]"
flake8 --exclude=setup.py --count app/blog-platform
