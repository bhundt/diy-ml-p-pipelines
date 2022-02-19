from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from playground import hello_world_job
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# scheduled pipelines
running_schedule = ScheduleDefinition(
    job=hello_world_job, cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

@repository
def get_jobs():
    return [hello_world_job, 
            deploy_job, 
            shell_job,
            running_schedule]
