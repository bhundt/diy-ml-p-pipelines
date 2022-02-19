#!/bin/bash

# settings
DIY_ML_P_ENVIRONMENT=local
DIY_ML_P_REL_DEPLOY_PATH=../../app

# check input
if [[ $# -eq 0 ]] ; then
    echo 'No argument given. Execute script with environment: dev, staging, prod'
    exit 1
fi

if [[ "$1" =~ ^(local)$ ]]; then
    echo ">>> Deploying: $1"
else
    echo "Wrong environment given! Deployment locally only!"
	exit 1
fi

read -p "Script intended to be run from pipelines repo main folder. Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "..exiting!"
    exit 1
fi

# clear working folder
echo ">> Removing current deployment"
rm -r $DIY_ML_P_REL_DEPLOY_PATH/$DIY_ML_P_ENVIRONMENT/pipelines/*

# copy to working folder
echo ">> Performing new deployment"
cp -a src/. $DIY_ML_P_REL_DEPLOY_PATH/$DIY_ML_P_ENVIRONMENT/pipelines/

echo ">> Installing config file for environment"
cd $DIY_ML_P_REL_DEPLOY_PATH/$DIY_ML_P_ENVIRONMENT/pipelines/conf/
cp config.$DIY_ML_P_ENVIRONMENT.yaml config.yaml
rm config.dev.yaml
rm config.staging.yaml
rm config.prod.yaml
rm config.local.yaml

# TODO: execute dagster
