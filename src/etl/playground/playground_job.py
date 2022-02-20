# execute with dagster job execute -f <FILE> -d <PATH OF FILE / WORKING DIR>
import os
from dagster import op, graph, ScheduleDefinition, DefaultScheduleStatus
from dagster.utils import file_relative_path

from utils.config import get_environment_config
from utils.helper import make_job

@op
def hello():
    print("Hello World!")
    print(os.getcwd())
    print(file_relative_path(__file__, './environments/schedules.yaml'))
    print(get_environment_config())

@graph
def hello_world():
    hello()

# schedule pipelines
running_schedule = ScheduleDefinition(
    job=make_job(hello_world), cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

def get_elements():
    return [make_job(hello_world), running_schedule]
