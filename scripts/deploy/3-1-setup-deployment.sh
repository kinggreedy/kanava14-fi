#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-1-setup-deployment

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# Create deployment path
sudo mkdir -p /opt/kanava14fi/shared/log
sudo mkdir -p /opt/kanava14fi/blog-platform
sudo chown -R deploy:deploy /opt/kanava14fi

# DONE
touch "$FLAG"
