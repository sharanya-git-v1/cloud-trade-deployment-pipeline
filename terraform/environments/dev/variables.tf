variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name used for AWS resource naming"
  type        = string
  default     = "cloud-trade-api"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}