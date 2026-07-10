# CI/CD Flow

This project uses GitHub Actions for CI automation.

## Current CI Pipeline

The current pipeline runs automatically on:

- Pushes to the `main` branch
- Pull requests

## Current Pipeline Steps

1. Checkout repository
2. Install .NET 8
3. Restore .NET dependencies
4. Build the .NET solution
5. Run automated tests
6. Install Python 3.12
7. Install Python dependencies
8. Validate environment config files

## Why This Matters

The CI pipeline acts as an automated quality gate. It ensures that code builds successfully, automated tests pass, and environment configuration files are valid before further deployment steps are added.

## Planned Future Steps

Later phases will extend the pipeline to include:

1. Docker image build
2. Docker image push to Amazon ECR
3. Terraform plan
4. AWS deployment
5. Smoke test after deployment