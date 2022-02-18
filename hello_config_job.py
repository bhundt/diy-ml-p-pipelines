# execute with dagster job execute -f hello_resource_job.py -c dev.yaml 
import os
from dagster import job, op, make_values_resource

@op(required_resource_keys={"values"})
def hello_config_op(context):
    print("Hello World!")
    print(os.getcwd())
    print(f"value: {context.resources.values['some_value']}")

@job(resource_defs={"values": make_values_resource()})
def hello_config_job():
    hello_config_op()
