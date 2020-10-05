#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags
DEPLOY_PATH=/opt/kanava14fi/app
SCRIPT_SUBPATH=/scripts/deploy

if [ ! -d "$FLAG" ]; then
  echo "$FLAG not exist, please run 0-account.sh manually"
  exit
fi

scripts=(
  "2-0-setup-common.sh"
  "2-1-setup-python.sh"
  "2-2-setup-postgres.sh"
  "2-3-setup-nginx.sh"
  "2-4-setup-redis.sh"
  "3-1-setup-deployment.sh"
  "4-1-run-predeploy.sh"
)

for script_name in ${scripts[*]}; do
  /bin/bash "$DEPLOY_PATH$SCRIPT_SUBPATH/$script_name"
done
