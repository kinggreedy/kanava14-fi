#!/usr/bin/env bash
set -euo pipefail

python -m pip install flake8
flake8 --exclude=setup.py --count app/blog-platform
