#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# TODO: Edit production.ini and start the process
pip install .
alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini

# DONE
sudo -u deploy touch "$FLAG"
