import os
from dagster import job, op, ScheduleDefinition, DefaultScheduleStatus

@op
def hello():
    print("Hello World!")
    print(os.getcwd())

@job
def hello_world_job():
    hello()

#running_schedule = ScheduleDefinition(
#    job=hello_world_job, cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
#)
