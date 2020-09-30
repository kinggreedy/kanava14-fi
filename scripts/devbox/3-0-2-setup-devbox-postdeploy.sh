#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-0-2-setup-devbox-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# TODO: Edit development.ini port 30486 listen to * and debugtoolbar.hosts
pserve development.ini --reload

# DONE
sudo -u deploy touch "$FLAG"
