#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive

python -m pip install .
alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini
# TODO: reload