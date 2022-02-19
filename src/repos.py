# Test with: dagster job execute -f ../../app/local/pipelines/etl/retrieve_stock_market_indicators_job.py -d ../../app/local/pipelines/
from dagster import ModeDefinition, repository, ScheduleDefinition, DefaultScheduleStatus, JobDefinition

from utils.helper import make_job_from_graph
from playground_job import hello_world_job, test_graph_job

# ops
from ops.deploy import deploy_job
from ops.shell_test import shell_job

# etl
from etl.retrieve_stock_market_indicators_job import retrieve_stock_market_indicators_job_schedule, retrieve_stock_market_indicators_job

# scheduled pipelines
running_schedule = ScheduleDefinition(
    job=make_job_from_graph(hello_world_job), cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

@repository
def get_etl_jobs():
    test_graph_job.to_job(name=test_graph_job.__name__ + "_dev")
    return [make_job_from_graph(hello_world_job), running_schedule,
            retrieve_stock_market_indicators_job, retrieve_stock_market_indicators_job_schedule]

@repository
def get_ops_jobs():
    return [deploy_job,
            shell_job]
