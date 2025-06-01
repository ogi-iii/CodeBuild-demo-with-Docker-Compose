# CodeBuild-demo-with-Docker-Compose
This is the demo project for AWS CodeBuild with Docker Compose.

# Requirements

- Python (3.13.3 or later)
- pip (25.1.1 or later)
- Docker (28.0.4 or later)

# Getting Started

## Run pytest locally

### 1. Install python packages

```bash
pip install -r requirements.txt
```

### 2. Run containers with Docker Compose

```bash
docker compose up -d
```

### 3. Run pytest

```bash
pytest
```

### 4. Stop and Remove containers with Docker Compose

```bash
docker compose down
```

## Run builds locally with the AWS CodeBuild agent

### 1. Install Docker images

```bash
# pull CodeBuild runtime container image
docker pull public.ecr.aws/codebuild/amazonlinux-x86_64-standard:5.0
# pull CodeBuild agent container image
docker pull public.ecr.aws/codebuild/local-builds:latest
```

### 2. Run the CodeBuild agent

```bash
./codebuild_build.sh -i public.ecr.aws/codebuild/amazonlinux-x86_64-standard:5.0 -a build/codebuild/
```
