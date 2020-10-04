#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.0-init
PASSWD="deploy"
PUBLIC_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAlpws4rTla3qLPY1UerUamLCxME5Um62NZDkGk13LboiM3WKkQrrkLyHBIreH+H0sWiVAWwOMtrwtIthqqys9I0eb377BAA3gRrlzS14l1P0x5Swzhe0qhq1aibr3piNjIEeciw9Ri9t6FT+1jng0kl5pXQjoSPIqIMu3ZqUAb1KAKm60LkReiIHEwr/ElWKCfcLXwb9OLlKPQIzlhZYJ6prNILE8fp1z2FYRoUmc4jnRwlAwnxReT9l63P6OJHfe2Cq2uyjR5F8wBPAn6lbb6Uz5fEae8p6l1MrX5HM8v0z3s57Cw30UFdmCnlChgF7/0n8lAhzQjqw9wh3KnFrwcQ== deploy"

if [ -f "$FLAG" ]; then
  echo "$FLAG exist, script has already run!"
  exit
fi

if [ "$PASSWD" = "deploy" ]; then
  echo "Password for deploy user need to be changed"
  exit
fi

# Create deployment user
for user in deploy
do
echo "Create sudo user $user"
sudo adduser --disabled-login --gecos "$user" "$user"
echo "$user:$PASSWD" | sudo chpasswd
sudo usermod -aG sudo "$user"
done

# Create deployment path
sudo mkdir -p /opt/kanava14fi/shared/log
sudo mkdir -p /opt/kanava14fi/flags
sudo mkdir -p /opt/kanava14fi/app/scripts/deploy
sudo mkdir -p /opt/kanava14fi/blog-platform
sudo chown -R deploy:deploy /opt/kanava14fi

# Add root permission for deploy user and ssh keys
sudo mkdir -p /home/deploy/.ssh
sudo touch /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 644 /home/deploy/.ssh/authorized_keys

sudo apt-get --ignore-missing install -y tee

echo "$PUBLIC_KEY" | sudo tee -a /home/deploy/.ssh/authorized_keys
echo 'deploy ALL=(ALL) NOPASSWD: ALL' | sudo tee -a /etc/sudoers

# DONE
sudo -u deploy touch "$FLAG"
