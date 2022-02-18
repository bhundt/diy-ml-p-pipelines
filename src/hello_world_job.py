import os
from dagster import job, op, ScheduleDefinition, DefaultScheduleStatus

@op
def hello():
    print("Hello World!")
    print(os.getcwd())

@job
def hello_world_job():
    hello()
