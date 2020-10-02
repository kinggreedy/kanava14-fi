#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive

cd /opt/kanava14fi
source venv/bin/activate

cd /opt/kanava14fi/blog-platform
python -m pip install .
alembic -c production.ini upgrade head

sudo service supervisor restart
