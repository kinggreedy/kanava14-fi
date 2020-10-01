#!/usr/bin/env bash

cd /opt/kanava14fi
source venv/bin/activate
cd /opt/kanava14fi/blog-platform
pserve development.ini --reload
