# DIY-ML-O pipelines
This repository holds all pipelines deployed to my DIY machine learning plattform (TODO put link to general description of DIY-ML-P). It is based on [dagster](https://dagster.io/).

## Repository Overview
```
repository/
├─ deployment/
├─ src/
│  ├─ etl/
│  ├─ ops/
│  ├─ repos.py
```
- `deployment/`: scripts for local and remote deployment.
- `src/etl`: files describing pipelines which performan data ingestion, transformation, ...
- `src/ops`: files describing pipelines which performan operations pipelines like deployments, ...
- `src/repos.py`: exports all pipelines to dagster.

## Deployment
We assume DIY-ML-P is accessible in the network under `diy-ml-p.local` and allows SSH connections. The assumed folder structure is created using [bhundt/diy-ml-p-infrastructure: Infrastructure repository for DIY-ML-P](https://github.com/bhundt/diy-ml-p-infrastructure) under `~/app/`. Execute `remote-deploy.sh <BRANCH>` in the main repository folder.