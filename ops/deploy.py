import os
from dagster import job, op

@op
def deploy_stuff():
    print("Deploy something!")

@job
def deploy_job():
    deploy_stuff()
