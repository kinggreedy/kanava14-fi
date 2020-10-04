#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags/.0-init
PASSWD="deploy"
PUBLIC_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCfUwZYXeI35sOy0VY6wmBRltmEIPk158OPsMwwGEGrmLQUtLQKF/e8N16NbxHfie3dehoD/dxPBX/OnIuiYsD7A5vC2h6ZYl+lYwrFgbKwIBEe5qrrLECxASIIQHaVQiHRzmBr6FNmcaZEg1QmgDuc+GVtL3hYDsConyUKpen12gyS58b+x5PlgwtAqnXzNfadfX2b/XuaVE/4EBfiFDlo/2IxbJxQi6DEqM91BWhp05LvpILTmY01jkV/TKP6AkGTWy8p+BvuuWiTTO8uuesEA7uTaLR2svuY949b3RKmzEZAHR1PE3Y1a8PJrCTIZ23ArLM6ThzgOm6W1BAFoy4lglV75fiBaqEWjCbLBeyQBLye5DWk9Gb34AIXwr5Yjix+L9xydA/PwP7/icJcb3XKm1l+ubIF/Q8X0UjY0QhCf+KcxsHoo79ibAGQankO3epX2MAEjRBAsVjNiOnl9eq2n8S8cAnkOvQuQLQ1666FH39EFRGjr1OHGvZyNQfbkuM="

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
sudo mkdir -p /opt/kanava14fi/app
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
touch "$FLAG"
