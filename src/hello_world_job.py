import os
from dagster import job, op
from dagster.utils import file_relative_path

@op
def hello():
    print("Hello World!")
    print(os.getcwd())
    print(file_relative_path(__file__, './environments/schedules.yaml'))

@job
def hello_world_job():
    hello()
