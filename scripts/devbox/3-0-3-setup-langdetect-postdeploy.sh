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
python -m pip install "celery[redis] < 5.0, >= 4.0"

# Config development.ini
CONFIG_INI_EXIST=$(grep "__languagedetectorapikey__" development.ini)
if [ ! $CONFIG_INI_EXIST ];
then
  /bin/cp -rf development.ini development.ini.bak
  /bin/cp -rf development.ini.sample development.ini
  read -d "\n" session_secret db_username db_password < /opt/kanava14fi/flags/.3-0-2-setup-devbox-postdeploy
  sudo sed -i "s/__secret__/$session_secret/g" development.ini
  sudo sed -i "s/__username__/$db_username/g" development.ini
  sudo sed -i "s/__password__/$db_password/g" development.ini
  sudo sed -i "s/__host__/localhost/g" development.ini
  sudo sed -i "s/__port__/5432/g" development.ini
  sudo sed -i "s/__table__/kanava14/g" development.ini
fi

sudo sed -i "s/__languagedetectorapikey__/demo/g" development.ini
sudo sed -i "s/__redissetupstring__/redis:\/\/localhost:6379\/0/g" development.ini

alembic -c development.ini upgrade head

# DONE
touch "$FLAG"
