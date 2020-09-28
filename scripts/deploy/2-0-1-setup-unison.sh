#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-0-1-setup-unison

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# SSH
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo service ssh restart

sudo apt-get -y install unison
curl -L -o unison-fsmonitor https://github.com/TentativeConvert/Syndicator/raw/master/unison-binaries/unison-fsmonitor
sudo mv unison-fsmonitor /usr/bin
sudo chmod +x /usr/bin/unison-fsmonitor

#TODO: priority ssh authentication
