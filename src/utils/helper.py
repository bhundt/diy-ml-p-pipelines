import os
from dagster import graph
from .config import get_environment_config

def make_job(graph, resource_def=None):
	env = get_environment_config()['env']
	return graph.to_job(name=graph.__name__ + "_" + env, resource_defs=resource_def)