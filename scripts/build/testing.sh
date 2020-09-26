#!/usr/bin/env bash
set -euo pipefail

python -m pip install pytest pytest-cov
pytest --cov-fail-under=60 --cov-report term --cov=app/blog-platform/blog_platform app/blog-platform
