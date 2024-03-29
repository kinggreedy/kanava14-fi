#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-0-2-setup-devbox-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

db_username=$(< /dev/urandom tr -dc a-z | head -c${1:-1})$(< /dev/urandom tr -dc a-z0-9 | head -c${1:-14})
db_password=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
session_secret=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER $db_username WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO $db_username;"

cd /opt/kanava14fi
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

python -m pip install --upgrade pip setuptools

cd /opt/kanava14fi/blog-platform
python -m pip install .
python -m pip install -e ".[develop]"

/bin/cp -rf development.ini.sample development.ini
sudo sed -i "s/__secret__/$session_secret/g" development.ini
sudo sed -i "s/__username__/$db_username/g" development.ini
sudo sed -i "s/__password__/$db_password/g" development.ini
sudo sed -i "s/__host__/localhost/g" development.ini
sudo sed -i "s/__port__/5432/g" development.ini
sudo sed -i "s/__table__/kanava14/g" development.ini

alembic -c development.ini upgrade head
initialize_blog_platform_db development.ini

# DONE
touch "$FLAG"
echo "$session_secret" | tee -a $FLAG
echo "$db_username" | tee -a $FLAG
echo "$db_password" | tee -a $FLAG
