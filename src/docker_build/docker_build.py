# config
# ops:
#   build_image:
#     config:
#       git_url: <GIT REPO URL>
#       branch: <BRANCH TO USE>
#       name: <IMAGE NAME: name:tag>
from logging.config import valid_ident
import os
import sys
import subprocess
import tempfile
from dagster import graph, op

from utils.config import get_environment_config
from utils.helper import make_job

def validate_url(url_to_validate: str) -> bool:
    import re
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url_to_validate) is not None # True
    

@op(config_schema={'git_url': str, 'branch': str, 'image_name': str, 'image_tag': str})
def build_image(context):
    git_url = context.op_config["git_url"]
    git_branch = context.op_config["branch"]
    image_name = context.op_config["image_name"]
    image_tag = context.op_config["image_tag"]

    if not validate_url(git_url):
        raise ValueError(f'Given git url {git_url} is invalid')

    context.log.info(f'Starting build from {git_url}:{git_branch}. Will create {image_name}:{image_tag}')

    # make temp directory
    with tempfile.TemporaryDirectory() as dirpath:
        context.log.info(f'Temporary directory: {str(dirpath)}')
        
        # clone git repository into temporary folder
        os.chdir(dirpath)
        if os.system(f'git clone -b {git_branch} {git_url} .') != 0:
            raise RuntimeError(f'Failed to clone git repository: {git_url} with branch {git_branch}')
        context.log.info('Git clone successfully executed')

        # execute docker build
        #if os.system(f'docker build -t {image_name}:{image_tag} .') != 0:
        #    raise RuntimeError(f'Failed to build image')
        try:
            subprocess.run([f'docker build -t {image_name}:{image_tag} .'], stdout=sys.stdout, stderr=sys.stderr, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Failed to build image')
        context.log.info('docker build successfully executed')

        


@graph
def docker_build():
    build_image()

def get_elements():
    return [make_job(docker_build)]