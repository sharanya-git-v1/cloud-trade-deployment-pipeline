# Cloud Trade Deployment Pipeline

This is a DevOps/CI/CD project that demonstrates how to automate the delivery of a small cloud application using GitHub Actions, Docker, Terraform, AWS, and Python automation scripts.

The application is intentionally simple. The main focus is the delivery workflow: validation, testing, containerization, infrastructure as code, cloud deployment, and smoke testing.

## Project Goal

Build a simple mock trade API and automate the delivery flow:

```text
Git commit
→ GitHub Actions CI pipeline
→ config validation
→ build and tests
→ Docker image build
→ Docker smoke test
→ push image to Amazon ECR
→ Terraform AWS deployment
→ ECS Fargate runtime
→ ALB smoke test
→ documentation
```

## Application

The app is a .NET 8 Minimal API with these endpoints:

- `/health` — health check endpoint
- `/version` — deployed app/version information
- `/config` — environment configuration
- `/trades` — mock trade data

## Tech Stack

- Git and GitHub
- GitHub Actions
- .NET 8 Minimal API
- xUnit tests
- Python automation scripts
- Docker
- Amazon ECR
- Amazon ECS Fargate
- Application Load Balancer
- CloudWatch Logs
- IAM / GitHub OIDC
- Terraform

## AWS Architecture

```text
User / Smoke Test
       ↓
Application Load Balancer
       ↓
ECS Fargate Service
       ↓
Docker container running .NET API
       ↓
Image pulled from Amazon ECR
       ↓
Logs sent to CloudWatch
```

## CI/CD Pipeline

The GitHub Actions pipeline is split into separate jobs:

1. Config Validation
2. Build and Test
3. Docker Smoke Test
4. Publish Image to Amazon ECR

On pushes to `main`, the pipeline builds the app, runs tests, validates config, builds the Docker image, smoke-tests the container, assumes an AWS IAM role using GitHub OIDC, and pushes the image to ECR.

## Infrastructure as Code

Terraform provisions the AWS resources, including:

- ECR repository
- ECR lifecycle policy
- GitHub Actions IAM role using OIDC
- ECS cluster
- ECS task definition
- ECS service
- ECS task execution role
- CloudWatch log group
- Application Load Balancer
- Target group
- Security groups

## Deployment Verification

The deployed app is verified using:

- Manual curl checks
- Browser checks against ALB DNS
- Python smoke test script
- Manual GitHub Actions deployment smoke test workflow

## Cost Safety

This project uses AWS resources that may incur charges, especially the Application Load Balancer and ECS Fargate runtime. Runtime resources are destroyed when not in use. AWS Budgets are configured to alert on spend.