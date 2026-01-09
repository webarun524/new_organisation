locals {
  merged_tags              = merge(var.tags, { Module = var.module_name })
  trusted_lambda_role_name = "${var.resource_prefix}-data-portal-access-role"
  ssm_format_service_name  = "/${replace(var.service_name, "-", "/")}"
  dp_password_secret_name  = "${local.ssm_format_service_name}/data-portal-password"
}
