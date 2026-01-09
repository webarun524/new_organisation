# Lambda - initial config

resource "aws_iam_policy" "config_lambda_ssm_sm_read" {
  name = "${var.resource_prefix}-lambda-ssm-sm-read"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = "arn:aws:secretsmanager:${var.aws_region}:*:secret:*"
      }
    ]
  })

  tags = local.merged_tags
}


# Lambda - password rotator

resource "aws_iam_policy" "rotator_assume_cognito_sm_policy" {
  name = "${var.resource_prefix}-lambda-cognito-password-rotator-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "RotatorAssumeCognitoSecretsSsmCrossRole"
        Effect   = "Allow"
        Action   = "sts:AssumeRole"
        Resource = "arn:aws:iam::*:role/${var.resource_prefix}-cognito-secrets-ssm-cross-role"
      },
      {
        Sid    = "RotatorSecretsManagerReadWrite"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:PutSecretValue",
          "secretsmanager:UpdateSecret",
          "secretsmanager:CreateSecret",
          "secretsmanager:DeleteSecret"
        ]
        Resource = "arn:aws:secretsmanager:${var.aws_region}:*:secret:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/*"
      },
    ]
  })

  tags = local.merged_tags
}
