# CI/CD Flow

This project uses GitHub Actions for CI and image publishing.

## Pipeline Jobs

### 1. Config Validation

Validates `config/dev.yml`, `config/uat.yml`, and `config/prod.yml` using a Python script.

This prevents invalid environment configuration from reaching deployment.

### 2. Build and Test

Restores .NET dependencies, builds the solution, and runs automated xUnit tests.

### 3. Docker Smoke Test

Builds the Docker image, starts the container, and checks `/health`.

This proves the packaged container actually runs.

### 4. Publish Image to ECR

On pushes to `main`, GitHub Actions assumes an AWS IAM role using OIDC, logs into Amazon ECR, and pushes the Docker image with:

- short Git commit SHA tag
- `latest` tag

## Deployment Smoke Test

A separate manual workflow runs a Python smoke test against the deployed ALB URL.

It validates:

- `/health`
- `/version`
- `/trades`