# config
# ops:
#   run_container:
#     config:
#       processing_job_name: <GIT REPO URL>
#       image_name: <BRANCH TO USE>
#       image_tag: <IMAGE NAME: name:tag>
#       path_data:
#       path_feature_store
from logging.config import valid_ident
import sys
import subprocess
from dagster import graph, op

from utils.config import get_environment_config
from utils.helper import make_job
    

@op(config_schema={'processing_job_name': str, 'image_name': str, 'image_tag': str, 'path_data': str, 'path_feature_store': str})
def run_container(context):
    processing_job_name = context.op_config["processing_job_name"]
    image_name = context.op_config["image_name"]
    image_tag = context.op_config["image_tag"]
    path_data = context.op_config["path_data"]
    path_feature_store = context.op_config["path_feature_store"]

    context.log.info(f'Starting processing job {processing_job_name} using {image_name}:{image_tag}.')
    context.log.info(f'Host data folder {path_data}.')
    context.log.info(f'Host feature-store folder {path_feature_store}.')

    try:
        command_to_run = f'docker run --name "{processing_job_name}" --rm -v "{path_data}":/data -v "{path_feature_store}":/feature-store {image_name}:{image_tag}'
        context.log.info(f'Running: "{command_to_run}"')
        subprocess.run(command_to_run, 
                        stdout=sys.stdout, 
                        stderr=sys.stderr, 
                        check=True, 
                        shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'Failed to run processing job {processing_job_name}')
    context.log.info('Processing job sucessfully executed.')

        


@graph
def run_processing_container():
    run_container()

def get_elements():
    return [make_job(run_processing_container)]