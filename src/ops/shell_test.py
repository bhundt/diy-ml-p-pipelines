from dagster import graph, job
from dagster_shell import create_shell_command_op

@graph
def shell_job():
    a = create_shell_command_op('echo "hello, world!"', name="a")
    b = create_shell_command_op('echo "hello, again!"', name="b")
    
    b(a())