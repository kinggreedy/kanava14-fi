#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-1-setup-deployment

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

#TODO: create deploy account

sudo mkdir -p /opt/python3test/blog-platform
sudo chown -R vagrant:vagrant /opt/python3test
ls -la /opt/python3test
cd /opt/python3test
virtualenv venv
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

pip install --upgrade pip setuptools

pip install .
