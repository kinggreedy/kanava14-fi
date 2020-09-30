#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-0-3-setup-acl

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# DONE
sudo -u deploy touch "$FLAG"
