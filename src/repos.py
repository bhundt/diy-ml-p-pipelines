# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from utils.helper import make_job
from playground_job import hello_world_job

# ops jobs
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# etl jobs
from etl.stock_market_indicators import retrieve_stock_market_indicators_job

# schedule pipelines
running_schedule = ScheduleDefinition(
    job=make_job(hello_world_job), cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)


@repository
def get_etl_jobs():
    return [make_job(hello_world_job), running_schedule,
            retrieve_stock_market_indicators_job.get_jobs(), retrieve_stock_market_indicators_job.get_scheduels()]

@repository
def get_ops_jobs():
    return [make_job(deploy_job),
            make_job(shell_job)]

@repository
def get_ml_jobs():
    return []
