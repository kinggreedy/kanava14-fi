#!/usr/bin/env bash

pip install .
alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini
