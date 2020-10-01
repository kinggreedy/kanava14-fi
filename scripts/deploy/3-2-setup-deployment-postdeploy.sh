#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

db_password=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
db_username=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
session_secret=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER $db_username WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO $db_username;"

cd /opt/kanava14fi
virtualenv venv
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

pip install --upgrade pip setuptools

cd /opt/kanava14fi/blog-platform
pip install .

sudo sed -i "s/__secret__/$session_secret/g" production.ini
sudo sed -i "s/__username__/$db_username/g" production.ini
sudo sed -i "s/__password__/$db_password/g" production.ini
sudo sed -i "s/__host__/localhost/g" production.ini
sudo sed -i "s/__port__/5432/g" production.ini
sudo sed -i "s/__table__/kanava14/g" production.ini

alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini

sudo cp scripts/deploy/resources/nginx_kanava14.conf /etc/nginx/sites-available/
sudo chmod 644 /etc/nginx/sites-available/nginx_kanava14.conf
sudo ln -s /etc/nginx/sites-available/nginx_kanava14.conf /etc/nginx/sites-enabled/nginx_kanava14.conf
sudo sed -i 's/# server_name  __additional_server_name__;/server_name  kanava14.kinggreedy.com;/g' /etc/ssh/sshd_config
sudo service nginx reload

# DONE
touch "$FLAG"
echo "$db_username" | tee -a $FLAG
echo "$db_password" | tee -a $FLAG
