#!/usr/bin/env bash

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
