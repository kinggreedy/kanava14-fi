#!/usr/bin/env bash

sudo apt-get -y install python-pip
sudo apt-get -y install virtualenv
sudo apt-get -y install python3.7 python3-pip

db_password=$(< /dev/urandom tr -dc _A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER kanava14 WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO kanava14;"
"
