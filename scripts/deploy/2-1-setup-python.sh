#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-1-setup-python

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt-get -y install \
    python-pip \
    python3.7 \
    python3-pip \
    virtualenv \
    supervisor

# DONE
touch "$FLAG"
