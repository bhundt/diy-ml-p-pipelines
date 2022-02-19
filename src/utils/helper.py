from dagster import graph
from config import get_environment_config

def make_job_from_graph(graph):
	env = utils.get_environment_config()['env']
	return graph.to_job(name=graph.__name__ + "_" + env)