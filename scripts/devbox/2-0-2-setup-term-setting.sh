#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-0-2-setup-personal-config

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

echo 'termcapinfo xterm ti@:te@' | tee -a ~/.screenrc

# DONE
sudo -u deploy touch "$FLAG"
