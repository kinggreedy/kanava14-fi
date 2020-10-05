#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-4-setup-redis

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt-get -y install redis-server

# DONE
touch "$FLAG"
