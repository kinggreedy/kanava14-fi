#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.0-init

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# Create deployment path
sudo mkdir -p /opt/kanava14fi/shared/log
sudo mkdir -p /opt/kanava14fi/flags
sudo chown -R vagrant:vagrant /opt/kanava14fi

# DONE
touch "$FLAG"
