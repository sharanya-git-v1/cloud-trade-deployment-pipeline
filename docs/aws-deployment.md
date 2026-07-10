# AWS Deployment Notes

## Overview

This project deploys a containerized .NET 8 Minimal API to AWS using Terraform.

The app is packaged as a Docker image, stored in Amazon ECR, and deployed to Amazon ECS Fargate behind an Application Load Balancer.

## AWS Resources

Terraform provisions the following AWS resources:

- Amazon ECR repository
- ECR lifecycle policy
- GitHub Actions OIDC provider
- IAM role for GitHub Actions ECR push
- ECS cluster
- ECS task definition
- ECS service
- ECS task execution role
- Application Load Balancer
- Target group
- Security groups
- CloudWatch log group

## Deployment Flow

```text
Docker image pushed to Amazon ECR
        ↓
ECS task definition references the ECR image
        ↓
ECS service starts one Fargate task
        ↓
Application Load Balancer forwards HTTP traffic to container port 8080
        ↓
/health endpoint confirms the deployment is working
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

## Useful Commands

### Apply infrastructure

```powershell
cd terraform\environments\dev
$env:AWS_PROFILE="personal"
terraform apply
```

### Wait for ECS service to become stable

```powershell
aws ecs wait services-stable `
  --cluster cloud-trade-api-dev-cluster `
  --services cloud-trade-api-dev-service `
  --region ap-southeast-1
```

### Get deployed app URLs

```powershell
terraform output -raw app_url
terraform output -raw health_check_url
```

### Test deployment manually

```powershell
$healthUrl = terraform output -raw health_check_url
$appUrl = terraform output -raw app_url

curl.exe $healthUrl
curl.exe "$appUrl/version"
curl.exe "$appUrl/trades"
```

### Run deployment smoke test script

```powershell
cd C:\Users\SNambiSaravanan\Documents\PersonalCode\cloud-trade-deployment-pipeline

cd terraform\environments\dev
$appUrl = terraform output -raw app_url
cd ..\..\..

python scripts\smoke_test.py --base-url $appUrl
```

## Deployment Verification

The deployed application was verified using:

- Browser check against the ALB `/health` endpoint
- Browser check against the ALB `/version` endpoint
- PowerShell `curl.exe` checks
- Python smoke test script
- GitHub Actions manual deployment smoke test workflow

The smoke test validates:

- `/health` returns `Healthy`
- `/version` returns the expected app name
- `/trades` returns mock trade data

## Cost Safety

The Application Load Balancer and ECS Fargate task can incur cost while running.

To pause the project safely, destroy only the runtime resources while keeping the ECR repository, Docker images, and GitHub Actions IAM/OIDC setup.

### Pause runtime resources

```powershell
cd C:\Users\SNambiSaravanan\Documents\PersonalCode\cloud-trade-deployment-pipeline\terraform\environments\dev
$env:AWS_PROFILE="personal"

$targets = @(
  "-target=aws_ecs_service.trade_api"
  "-target=aws_ecs_task_definition.trade_api"
  "-target=aws_ecs_cluster.trade_api"
  "-target=aws_lb_listener.http"
  "-target=aws_lb_target_group.trade_api"
  "-target=aws_lb.trade_api"
  "-target=aws_security_group.ecs_tasks"
  "-target=aws_security_group.alb"
  "-target=aws_cloudwatch_log_group.trade_api"
  "-target=aws_iam_role_policy_attachment.ecs_task_execution"
  "-target=aws_iam_role.ecs_task_execution"
)

terraform destroy @targets
```

This removes the higher-cost runtime resources:

- ECS service
- Fargate task
- ECS cluster
- Application Load Balancer
- Target group
- Runtime security groups
- CloudWatch log group
- ECS task execution role

This keeps the lower-cost/supporting resources:

- ECR repository
- ECR images
- ECR lifecycle policy
- GitHub Actions OIDC provider
- GitHub Actions IAM role for ECR push

### Resume later

To recreate the runtime deployment:

```powershell
cd C:\Users\SNambiSaravanan\Documents\PersonalCode\cloud-trade-deployment-pipeline\terraform\environments\dev
$env:AWS_PROFILE="personal"
terraform apply
```

## Notes

A full `terraform destroy` would delete everything Terraform manages, including the ECR repository and GitHub Actions IAM/OIDC setup.

For this project, the preferred cost-safe pause method is the targeted runtime destroy shown above.