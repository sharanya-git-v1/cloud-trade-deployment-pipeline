locals {
  github_owner  = "sharanya-git-v1"
  github_repo   = "cloud-trade-deployment-pipeline"
  github_branch = "main"

  github_oidc_subject = "repo:${local.github_owner}/${local.github_repo}:ref:refs/heads/${local.github_branch}"
}

resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.github_actions.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        local.github_oidc_subject
      ]
    }
  }
}

resource "aws_iam_role" "github_actions_ecr_push" {
  name = "${var.project_name}-${var.environment}-github-actions-ecr-push-role"

  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json

  tags = local.common_tags
}

data "aws_iam_policy_document" "github_actions_ecr_push" {
  statement {
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken"
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeRepositories",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart"
    ]

    resources = [
      aws_ecr_repository.trade_api.arn
    ]
  }
}

resource "aws_iam_role_policy" "github_actions_ecr_push" {
  name = "${var.project_name}-${var.environment}-github-actions-ecr-push-policy"
  role = aws_iam_role.github_actions_ecr_push.id

  policy = data.aws_iam_policy_document.github_actions_ecr_push.json
}