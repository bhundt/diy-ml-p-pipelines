import yaml
from dagster.utils import file_relative_path

def get_environment_config():
    with open(file_relative_path(__file__, "config.dev.yaml"), "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)