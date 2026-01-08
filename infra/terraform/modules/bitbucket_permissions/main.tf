resource "aws_iam_openid_connect_provider" "bitbucket" {
  url             = var.bitbucket_oidc_provider_url
  client_id_list  = [var.bitbucket_audience]
  thumbprint_list = [var.bitbucket_thumbprint]
  tags            = local.merged_tags
}

resource "aws_iam_policy" "bitbucket_sfn_exec_policy" {
  name        = "${var.resource_prefix}-bitbucket-sfn-exec-policy"
  description = "Allows Bitbucket to start the E2E Step Function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "states:StartExecution"
        Resource = var.sfn_orchestrator_arn
      },
    ]
  })

  tags = local.merged_tags
}

resource "aws_iam_role" "bitbucket_sfn_exec_role" {
  name                 = "${var.resource_prefix}-bitbucket-sfn-exec-role"
  assume_role_policy   = data.aws_iam_policy_document.bitbucket_assume_role.json
  max_session_duration = var.max_session_duration
  tags                 = local.merged_tags
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "bitbucket_sfn_exec_attach" {
  role       = aws_iam_role.bitbucket_sfn_exec_role.name
  policy_arn = aws_iam_policy.bitbucket_sfn_exec_policy.arn
}
