#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-0-3-setup-langdetect-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

cd /opt/kanava14fi
source venv/bin/activate

cd /opt/kanava14fi/blog-platform
python -m pip install .
python -m pip install -U "celery[redis]"

# Config development.ini
if [ ! grep -q "__languagedetectorapikey__" development.ini; ]
then
  /bin/cp -rf development.ini development.ini.bak
  /bin/cp -rf development.ini.sample development.ini
  read -d "\n" session_secret db_username db_password < /opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy
  sudo sed -i "s/__secret__/$session_secret/g" development.ini
  sudo sed -i "s/__username__/$db_username/g" development.ini
  sudo sed -i "s/__password__/$db_password/g" development.ini
  sudo sed -i "s/__host__/localhost/g" development.ini
  sudo sed -i "s/__port__/5432/g" development.ini
  sudo sed -i "s/__table__/kanava14/g" development.ini
fi

sudo sed -i "s/__languagedetectorapikey__/demo/g" development.ini
sudo sed -i "s/__redissetupstring__/redis:\/\/localhost:6379\/0/g" development.ini

# DONE
touch "$FLAG"
