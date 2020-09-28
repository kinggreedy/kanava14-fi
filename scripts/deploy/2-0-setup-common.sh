#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-0-setup-common

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get -y autoremove
sudo apt-get -y autoclean
