# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from playground_job import hello_world_job

# ops
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# etl
from etl.retrieve_stock_market_indicators_job import retrieve_stock_market_indicators_job_schedule, retrieve_stock_market_indicators_job

# scheduled pipelines
running_schedule = ScheduleDefinition(
    job=hello_world_job, cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

@repository
def get_etl_jobs():
    return [hello_world_job, running_schedule,
            retrieve_stock_market_indicators_job, retrieve_stock_market_indicators_job_schedule]

@repository
def get_ops_jobs():
    return [deploy_job,
            shell_job]
