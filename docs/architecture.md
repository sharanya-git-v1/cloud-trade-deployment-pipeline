# Architecture

## Current Phase

The project currently contains the base repository structure, configuration files, and documentation placeholders.

## Final Target Architecture

```text
Developer
   ↓
GitHub Repository
   ↓
GitHub Actions Pipeline
   ↓
Tests + Config Validation + Docker Build
   ↓
Amazon ECR
   ↓
Terraform
   ↓
Amazon ECS Fargate
   ↓
Application Load Balancer
   ↓
Smoke Test
```

## Design Principle

The application is intentionally simple. The main purpose of this project is to demonstrate a realistic DevOps delivery workflow.