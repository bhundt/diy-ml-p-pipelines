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
mkdir tmp_deploy_feature_store
cd tmp_deploy_feature_store

echo ">>> Cloning $BRANCH branch"
git clone --branch $BRANCH https://github.com/bhundt/diy-ml-p-feature-store.git
cd diy-ml-p-feature-store

# clear working folder
echo ">>> Removing current deployment"
rm -r ~/$APP_PATH/$ENV/feature-store/*

# copy to working folder
echo ">>> Dopying new files"
cp -a src/. ~/$APP_PATH/$ENV/feature-store/

# feast apply
echo ">>> Applying changes"
cd ~/$APP_PATH/$ENV/feature-store/
feast apply

echo ">>> Removing temp files"
rm -rf ~/tmp_deploy_feature_store/
exit
EOF

echo ">>> ...Done!"