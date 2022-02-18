from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from hello_world_job import hello_world_job
from ops.deploy import deploy_job

running_schedule = ScheduleDefinition(
    job=hello_world_job, cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

@repository
def get_dev_repos():
    return [hello_world_job, deploy_job, running_schedule]
