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

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.trade_api.dns_name
}

output "app_url" {
  description = "Public URL of the deployed application"
  value       = "http://${aws_lb.trade_api.dns_name}"
}

output "health_check_url" {
  description = "Health check URL of the deployed application"
  value       = "http://${aws_lb.trade_api.dns_name}/health"
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.trade_api.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.trade_api.name
}

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group for ECS task logs"
  value       = aws_cloudwatch_log_group.trade_api.name
}