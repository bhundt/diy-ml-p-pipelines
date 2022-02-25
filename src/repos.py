# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import repository, ScheduleDefinition, DefaultScheduleStatus

from utils.helper import make_job

# ops jobs
from ops.deploy import deploy_job
from ops.shell_test import shell_job
from docker_build import docker_build
from run_processing_container import run_processing_container

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
    all_ops_jobs = []
    all_ops_jobs.extend( [make_job(deploy_job), make_job(shell_job)] )
    all_ops_jobs.extend( docker_build.get_elements() )
    all_ops_jobs.extend( run_processing_container.get_elements() )

    return all_ops_jobs

@repository
def get_ml_jobs():
    return []
