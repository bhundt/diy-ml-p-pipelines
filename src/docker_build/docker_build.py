# config
# ops:
#   build_image:
#     config:
#       git_url: <GIT REPO URL>
#       branch: <BRANCH TO USE>
#       name: <IMAGE NAME: name:tag>
import os
from dagster import graph, op

from utils.config import get_environment_config
from utils.helper import make_job

@op(config_schema={'git_url': str, 'branch': str, 'image_name': str, 'image_tag': str})
def build_image(context):
    print(f'GIT URL: {context.op_config["git_url"]}')
    print(f'GIT BRANCH: {context.op_config["branch"]}')
    print(f'IMAGE NAME: {context.op_config["image_name"]}')
    print(f'IMAGE TAG: {context.op_config["image_tag"]}')

@graph
def docker_build():
    build_image()

def get_elements():
    return [make_job(docker_build)]