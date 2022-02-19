# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from utils.helper import make_job
from playground_job import hello_world_job

# ops jobs
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# etl jobs
from etl.retrieve_stock_market_indicators_job import retrieve_stock_market_indicators_job

# scheduled pipelines
running_schedule = ScheduleDefinition(
    job=make_job(hello_world_job), cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

retrieve_stock_market_indicators_job_schedule = ScheduleDefinition(
    job=make_job(retrieve_stock_market_indicators_job), cron_schedule="0 6 * * 2-6", default_status=DefaultScheduleStatus.RUNNING
)

@repository
def get_etl_jobs():
    return [make_job(hello_world_job), running_schedule,
            make_job(retrieve_stock_market_indicators_job), retrieve_stock_market_indicators_job_schedule]

@repository
def get_ops_jobs():
    return [make_job(deploy_job),
            make_job(shell_job)]
