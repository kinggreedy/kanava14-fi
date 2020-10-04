#!/usr/bin/env bash
set -euo pipefail

cd app/blog-platform
python -m pip install -e ".[testing]"
pytest --cov-fail-under=60 --cov-report term --cov=./blog_platform .
