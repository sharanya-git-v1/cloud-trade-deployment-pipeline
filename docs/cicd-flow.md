# CI/CD Flow

The planned CI/CD flow is:

1. Developer pushes code to GitHub.
2. GitHub Actions starts automatically.
3. Pipeline validates config files.
4. Pipeline runs automated tests.
5. Pipeline builds the application.
6. Pipeline builds a Docker image.
7. Later, the image will be pushed to Amazon ECR.
8. Later, Terraform will deploy the infrastructure and application to AWS.
9. A smoke test will verify that the deployed app is healthy.