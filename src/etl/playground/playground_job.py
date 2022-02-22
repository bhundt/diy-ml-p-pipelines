# config
# ops:
#   hello:
#     config:
#       test: 1
# resources:
#   values:
#     config:
#       my_int: 10
#       my_str: hallo
import os
from dagster import op, graph, ScheduleDefinition, DefaultScheduleStatus, make_values_resource
from dagster.utils import file_relative_path

from utils.config import get_environment_config
from utils.helper import make_job

@op(config_schema={"test": int}, required_resource_keys={"values"})
def hello(context):
    print("Hello World!")
    print(os.getcwd())
    print(file_relative_path(__file__, './environments/schedules.yaml'))
    print(get_environment_config())
    print(context.op_config["test"])
    print(context.resources.values['my_str'])
    print(context.resources.values['my_int'])

@graph
def hello_world():
    hello()

# schedule pipelines
#running_schedule = ScheduleDefinition(
#    job=make_job(hello_world), cron_schedule="*/3 * * * *", default_status=DefaultScheduleStatus.RUNNING
#)

def get_elements():
    #return [hello_world.to_job(resource_defs={"values": make_values_resource(my_str=str, my_int=int)})]
    return [make_job(hello_world, resource_defs={"values": make_values_resource(my_str=str, my_int=int)})]
