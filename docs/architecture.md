# Architecture

## Overview

This project deploys a small .NET 8 Minimal API to AWS using a DevOps-style delivery workflow.

The application image is built with Docker, stored in Amazon ECR, and deployed to Amazon ECS Fargate using Terraform.

## Architecture Diagram

```text
Developer
   ↓
GitHub Repository
   ↓
GitHub Actions
   ↓
Config Validation + Build + Tests
   ↓
Docker Build + Container Smoke Test
   ↓
Amazon ECR
   ↓
Terraform
   ↓
Amazon ECS Fargate
   ↓
Application Load Balancer
   ↓
Public API Endpoint
```

## Runtime Architecture

```text
Internet
   ↓
Application Load Balancer :80
   ↓
Target Group :8080
   ↓
ECS Fargate Task
   ↓
cloud-trade-api container
   ↓
CloudWatch Logs
```

## Design Decisions

- The app is simple because the focus is DevOps automation.
- ECR stores the Docker image before ECS deployment.
- ECS Fargate avoids managing EC2 servers.
- ALB exposes the app publicly and performs health checks.
- Terraform manages infrastructure as code.
- GitHub Actions uses OIDC instead of long-lived AWS keys.