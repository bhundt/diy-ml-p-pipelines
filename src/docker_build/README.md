# docker_build job

dagster job for cloning a git repo and building a docker image from that repo.

**Example Config**
```yaml
ops:
  build_image:
    config:
      git_url: "https://github.com/bhundt/processing_container_template.git"
      branch: "main"
      image_name: "processing-container-template"
      image_tag: "0.0.1"
```