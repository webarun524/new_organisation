/* Lambda - initial tests config */

module "config_composer_lambda_function" {
  source = "../lambda_function"

  function_name     = local.function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/config_composer"
  handler           = "lambdas.config_composer.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]
  extra_policy_arns = [
    aws_iam_policy.config_lambda_ssm_sm_read.arn,
  ]

  environment_variables = {
    LOG_LEVEL       = "INFO"
    REQUEST_TIMEOUT = "20.0"
    SERVICE_NAME    = var.service_name
  }

  tags        = local.merged_tags
  module_name = var.module_name
}

/* SSM & SM */

resource "aws_ssm_parameter" "test_admin_user_name" {
  name  = local.test_admin_user_name_parameter_name
  type  = "String"
  value = local.e2e_test_account_admin_name
}

resource "aws_ssm_parameter" "test_operations_portal_url" {
  name  = local.operations_portal_url_parameter_name
  type  = "String"
  value = local.operations_portal_url
}

resource "aws_ssm_parameter" "test_inbox_address" {
  name  = local.test_inbox_address_parameter_name
  type  = "String"
  value = local.test_inbox_address
}

resource "aws_secretsmanager_secret" "test_admin_user_password" {
  name = local.test_admin_user_password_secret_name
}

resource "aws_secretsmanager_secret_version" "test_admin_user_password_value" {
  secret_id     = aws_secretsmanager_secret.test_admin_user_password.id
  secret_string = "sensitive_value_changed_in_aws_console"

  lifecycle {
    ignore_changes = [
      secret_string,
    ]
  }
}

resource "aws_secretsmanager_secret" "test_inbox_password" {
  name = local.test_inbox_password_secret_name
}

resource "aws_secretsmanager_secret_version" "test_inbox_password_value" {
  secret_id     = aws_secretsmanager_secret.test_inbox_password.id
  secret_string = "sensitive_value_changed_in_aws_console"

  lifecycle {
    ignore_changes = [
      secret_string,
    ]
  }
}

resource "aws_ssm_parameter" "bb_env_code" {
  name  = local.bb_env_code_parameter_name
  type  = "String"
  value = local.bb_env_code
}

resource "aws_ssm_parameter" "bb_env_name" {
  name  = local.bb_env_name_parameter_name
  type  = "String"
  value = local.bb_env_name
}

/* Lambda - Data Portal password rotator */

module "dp_password_rotator_lambda_function" {
  source = "../lambda_function"

  function_name     = local.dp_password_rotator_function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/dp_password_rotator"
  handler           = "lambdas.dp_password_rotator.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]
  extra_policy_arns = [
    aws_iam_policy.rotator_assume_cognito_sm_policy.arn,
  ]

  environment_variables = {
    LOG_LEVEL                              = "INFO"
    REQUEST_TIMEOUT                        = "20.0"
    DP_TEMP_PASSWORD_SECRET_NAME           = local.dp_temp_password_secret_name
    DP_PASSWORD_SECRET_NAME                = local.dp_password_secret_name
    DP_COGNITO_USER_POOL_ID_PARAMETER_NAME = local.dp_cognito_user_pool_id_parameter_name
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
