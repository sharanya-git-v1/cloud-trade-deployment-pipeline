output "aws_account_id" {
  description = "AWS account ID used by Terraform"
  value       = data.aws_caller_identity.current.account_id
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.trade_api.name
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.trade_api.repository_url
}

output "github_actions_role_arn" {
  description = "IAM role ARN used by GitHub Actions to push images to ECR"
  value       = aws_iam_role.github_actions_ecr_push.arn
}