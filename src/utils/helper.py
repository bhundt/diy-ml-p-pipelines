from dagster import graph

def make_job_from_graph(graph):
	env = utils.get_config()['env']
	return graph.to_job(name=graph.__name__ + "_" + env)