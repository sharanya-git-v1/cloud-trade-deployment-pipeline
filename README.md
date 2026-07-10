# Cloud Trade Deployment Pipeline

This is a portfolio DevOps/CI/CD project that demonstrates how to automate the deployment of a small cloud application using GitHub Actions, Docker, Terraform, AWS, and Python automation scripts.

## Project Goal

Build a simple mock trade API and automate the delivery flow:

```text
Git commit
→ GitHub Actions CI pipeline
→ tests
→ config validation
→ build/package
→ Docker image
→ Terraform infrastructure provisioning
→ AWS deployment
→ smoke test
→ documentation
```

## Application

The application will be a simple .NET 8 Minimal API with endpoints such as:

- `/health`
- `/version`
- `/config`
- `/trades`

The app is intentionally simple because the main focus is DevOps automation.

## Target Skills

This project is designed to practise:

- Git and GitHub
- GitHub Actions
- .NET 8
- Docker
- Python automation
- Terraform
- AWS deployment
- Smoke testing
- Technical documentation

## Planned AWS Architecture

The final deployment target will use:

- Amazon ECR
- Amazon ECS Fargate
- Application Load Balancer
- CloudWatch Logs
- IAM roles
- Terraform-managed infrastructure

## Project Phases

1. Phase 0 — Project setup and repo structure
2. Phase 1 — Create local API
3. Phase 2 — Add automated tests
4. Phase 3 — Add config validation script
5. Phase 4 — Add GitHub Actions CI pipeline
6. Phase 5 — Dockerize the app
7. Phase 6 — Add Terraform AWS infrastructure
8. Phase 7 — Deploy to AWS
9. Phase 8 — Smoke test and documentation