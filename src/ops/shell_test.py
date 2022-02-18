from dagster import op, job
from dagster_shell import create_shell_command_op

@job
def shell_job():
    a = create_shell_command_op('echo "hello, world!"', name="a")
    a()

    b = create_shell_command_op('echo "hello, again!"', name="b")
    b()