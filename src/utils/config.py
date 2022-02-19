import yaml
from dagster.utils import file_relative_path

def get_environment_config():
    with open(file_relative_path(__file__, "../conf/config.yaml"), "r") as stream:
        try:
            return yaml.safe_load(stream)['config']
        except yaml.YAMLError as exc:
            print("Failed to load environment config.yaml!")
            raise