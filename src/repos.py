# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from utils.helper import make_job

# ops jobs
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# etl jobs
from etl.playground import playground_job
from etl.stock_market_indicators import retrieve_stock_market_indicators_job


@repository
def get_etl_jobs():
    all_etl_jobs = []
    all_etl_jobs.extend( playground_job.get_elements() )
    all_etl_jobs.extend( retrieve_stock_market_indicators_job.get_elements() )

    return all_etl_jobs

@repository
def get_ops_jobs():
    return [make_job(deploy_job),
            make_job(shell_job)]

@repository
def get_ml_jobs():
    return []
