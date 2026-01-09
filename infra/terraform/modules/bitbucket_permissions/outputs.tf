output "bitbucket_role_configuration" {
  description = "Summary of Bitbucket Pipelines role configuration"
  value = {
    role_name     = aws_iam_role.bitbucket_sfn_exec_role.name
    role_arn      = aws_iam_role.bitbucket_sfn_exec_role.arn
    role_id       = aws_iam_role.bitbucket_sfn_exec_role.id
    account_id    = data.aws_caller_identity.current.account_id
    region        = data.aws_region.current.name
    oidc_provider = aws_iam_openid_connect_provider.bitbucket.arn
  }
}
