# run_processing_container

dagster job for running a [processing container](https://github.com/bhundt/processing_container_template).

**Example Config**





- **Run**: `docker run --name "processing_job" --rm -v :/data -v :/feature-store processing_job:0.0.1`