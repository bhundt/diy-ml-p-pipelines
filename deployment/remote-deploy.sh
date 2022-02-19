#!/bin/bash
# This script pushes dev, staging, prod to GitHub as well as to production server.

# settings
APP_PATH=app
ENV=$1
BRANCH=$ENV

# check input
if [[ $# -eq 0 ]] ; then
    echo 'No argument given. Execute script with environment: dev, staging, prod'
    exit 1
fi

if [[ "$ENV" == "prod" ]]; then
	BRANCH=main
fi

if [[ "$1" =~ ^(dev|staging|prod)$ ]]; then
    echo ">>> Starting deployment to $ENV based on branch $BRANCH"
else
    echo "Wrong environment given! Environment needs to be dev, staging or prod"
	exit 1
fi


# push changes
echo ">>> Pushing $1 to GitHub"
git push origin $BRANCH

# Log in to DIY-ML-P
echo ">>> Log into DIY-ML-P"
ssh pi@diy-ml-p.local << EOF

# Temp folder
echo ">>> Create temp folder"
cd ~/
mkdir tmp_deploy_pipelines
cd tmp_deploy_pipelines

echo ">>> Cloning $BRANCH branch"
git clone --branch $BRANCH https://github.com/bhundt/diy-ml-p-pipelines.git
cd diy-ml-p-pipelines

# clear working folder
echo ">>> Removing current deployment"
rm -rf ~/$APP_PATH/$ENV/pipelines/*

# copy to working folder
echo ">>> Copying new files"
cp -a src/. ~/$APP_PATH/$ENV/pipelines/

# installing config file
echo ">>> Installing config file for environment"
cd  ~/$APP_PATH/$ENV/pipelines/
cp config.$ENV.yaml config.yaml
rm config.dev.yaml
rm config.staging.yaml
rm config.prod.yaml

# restart scheduler
echo ">>> Applying changes"
sudo systemctl stop dagit
sudo systemctl stop dagster
sudo systemctl start dagster
sudo systemctl start dagit
cd ~/

echo ">>> Removing temp files"
rm -rf ~/tmp_deploy_pipelines/
exit
EOF

echo ">>> ...Done!"