data "aws_iam_policy_document" "bitbucket_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.bitbucket.arn]
    }

    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "${replace(var.bitbucket_oidc_provider_url, "https://", "")}:aud"
      values   = [var.bitbucket_audience]
    }

    condition {
      test     = "StringLike"
      variable = "${replace(var.bitbucket_oidc_provider_url, "https://", "")}:sub"
      values   = var.bitbucket_subjects
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
