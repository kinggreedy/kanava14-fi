#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.2-2-setup-postgres

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list
cat /etc/apt/sources.list.d/pgdg.list
sudo apt-get update
sudo apt-get -y install postgresql-11

db_password=$(< /dev/urandom tr -dc _A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER kanava14 WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO kanava14;"
"

#TODO: write username and password to temporally file
