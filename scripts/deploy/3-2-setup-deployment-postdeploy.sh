#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.3-2-setup-deployment-postdeploy

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

export DEBIAN_FRONTEND=noninteractive

# Setup database user
db_username=$(< /dev/urandom tr -dc a-z | head -c${1:-1})$(< /dev/urandom tr -dc a-z0-9 | head -c${1:-14})
db_password=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
session_secret=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-15})
sudo -u postgres psql -c "CREATE DATABASE kanava14;"
sudo -u postgres psql -c "
    CREATE USER $db_username WITH ENCRYPTED PASSWORD '$db_password';
    GRANT ALL PRIVILEGES ON DATABASE kanava14 TO $db_username;"

# Setup python env
cd /opt/kanava14fi
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

python -m pip install --upgrade pip setuptools

cd /opt/kanava14fi/blog-platform
python -m pip install .

# Config production.ini
/bin/cp -rf production.ini.sample production.ini
sudo sed -i "s/__secret__/$session_secret/g" production.ini
sudo sed -i "s/__username__/$db_username/g" production.ini
sudo sed -i "s/__password__/$db_password/g" production.ini
sudo sed -i "s/__host__/localhost/g" production.ini
sudo sed -i "s/__port__/5432/g" production.ini
sudo sed -i "s/__table__/kanava14/g" production.ini

alembic -c production.ini upgrade head
initialize_blog_platform_db production.ini

# Config nginx
sudo ln -s /opt/kanava14fi/blog-platform/blog_platform /var/www/kanava14fi
sudo ln -s /opt/kanava14fi/blog-platform/nginx.conf /etc/nginx/sites-available/kanava14fi.conf
sudo chmod 644 /etc/nginx/sites-available/kanava14fi.conf
sudo ln -s /etc/nginx/sites-available/kanava14fi.conf /etc/nginx/sites-enabled/kanava14fi.conf
mkdir -p /opt/kanava14fi/shared/log
sudo service nginx reload

# Config supervisor
sudo ln -s  /opt/kanava14fi/blog-platform/supervisord.conf /etc/supervisor/conf.d/kanava14fi.conf
sudo service supervisor restart

# DONE
touch "$FLAG"
echo "$db_username" | tee -a $FLAG
echo "$db_password" | tee -a $FLAG
