#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags
DEPLOY_PATH=/opt/kanava14fi/app
SCRIPT_SUBPATH=/bash

if [ ! -d "$FLAG" ]; then
  echo "$FLAG not exist, please run 0-account.sh manually"
  exit
fi

for script_name in 2-0-setup-common.sh 2-1-setup-python 2-2-setup-postgres.sh 3-1-setup-deployment.sh 3-2-setup-deployment-postdeploy.sh 4-1-run-predeploy.sh 4-2-run-postdeploy.sh
do
/bin/bash "$DEPLOY_PATH$SCRIPT_SUBPATH/$script_name"
done
