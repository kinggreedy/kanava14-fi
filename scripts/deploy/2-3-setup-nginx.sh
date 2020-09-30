#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-3-setup-nginx

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# TODO

# DONE
sudo -u deploy touch "$FLAG"
