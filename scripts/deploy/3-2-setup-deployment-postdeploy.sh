#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# TODO: Edit production.ini and start the process
pip install .
alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini

db_password=$(< /dev/urandom tr -dc _A-Za-z0-9 | head -c${1:-15})
db_username=$(< /dev/urandom tr -dc _A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER $db_username WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO $db_username;"

sudo -u deploy touch "$FLAG"
echo "$db_username" | tee -a $FLAG
echo "$db_password" | tee -a $FLAG

sudo cp scripts/deploy/resources/nginx_kanava14.conf /etc/nginx/sites-available/
sudo chmod 644 /etc/nginx/sites-available/nginx_kanava14.conf
sudo ln -s /etc/nginx/sites-available/nginx_kanava14.conf /etc/nginx/sites-enabled/nginx_kanava14.conf
sudo sed -i 's/# server_name  __additional_server_name__;/server_name  kanava14.kinggreedy.com;/g' /etc/ssh/sshd_config
sudo service nginx reload

# DONE
sudo -u deploy touch "$FLAG"
