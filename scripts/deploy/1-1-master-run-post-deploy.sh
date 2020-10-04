#!/usr/bin/env bash

FLAG=/opt/kanava14fi/flags
DEPLOY_PATH=/opt/kanava14fi/app
SCRIPT_SUBPATH=/scripts/deploy

if [ ! -d "$FLAG" ]; then
  echo "$FLAG not exist, please run 0-account.sh manually"
  exit
fi

scripts=(
  "3-2-setup-deployment-postdeploy.sh"
  "4-2-run-postdeploy.sh"
)

for script_name in ${scripts[*]}; do
  /bin/bash "$DEPLOY_PATH$SCRIPT_SUBPATH/$script_name"
done
