# execute with dagster job execute -f <FILE> -d <PATH OF FILE / WORKING DIR>
import os
from dagster import job, op
from dagster.utils import file_relative_path

from utils import get_environment_config

@op
def hello():
    print("Hello World!")
    print(os.getcwd())
    print(file_relative_path(__file__, './environments/schedules.yaml'))
    print(get_environment_config())

@job
def hello_world_job():
    hello()
