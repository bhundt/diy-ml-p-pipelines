from dagster import graph, op

from utils.config import get_environment_config

@op
def deploy_stuff():
    print("Deploy something!")
    print(get_environment_config())

@graph
def deploy_job():
    deploy_stuff()
