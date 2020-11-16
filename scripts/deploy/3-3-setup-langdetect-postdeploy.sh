#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-3-setup-langdetect-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

cd /opt/kanava14fi
source venv/bin/activate

cd /opt/kanava14fi/blog-platform
python -m pip install .
python -m pip install "celery[redis] < 5.0, >= 4.0"

# Config production.ini
CONFIG_INI_EXIST=$(grep "__languagedetectorapikey__" production.ini)
if [ ! $CONFIG_INI_EXIST ];
then
  /bin/cp -rf production.ini production.ini.bak
  /bin/cp -rf production.ini.sample production.ini
  read -d "\n" session_secret db_username db_password < /opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy
  sudo sed -i "s/__secret__/$session_secret/g" production.ini
  sudo sed -i "s/__username__/$db_username/g" production.ini
  sudo sed -i "s/__password__/$db_password/g" production.ini
  sudo sed -i "s/__host__/localhost/g" production.ini
  sudo sed -i "s/__port__/5432/g" production.ini
  sudo sed -i "s/__table__/kanava14/g" production.ini
fi

if [ ! -z "$LANGUAGE_DETECTOR_API_KEY" ]; then
  sudo sed -i "s/__languagedetectorapikey__/$LANGUAGE_DETECTOR_API_KEY/g" production.ini
fi

sudo sed -i "s/__redissetupstring__/redis:\/\/localhost:6379\/0/g" production.ini

# DONE
touch "$FLAG"
