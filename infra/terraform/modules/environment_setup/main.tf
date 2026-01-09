module "setup_trigger_lambda_function" {
  source = "../lambda_function"

  function_name     = "setup-trigger"
  lambda_source_dir = "${path.module}/../../../../src/lambdas/setup_trigger"
  handler           = "lambdas.setup_trigger.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.setup_lambda_timeout
  memory_size    = var.setup_lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  environment_variables = {
    LOG_LEVEL       = "INFO"
    REQUEST_TIMEOUT = "30"
    BITBUCKET_TOKEN = var.bitbucket_token
  }

  tags        = local.merged_tags
  module_name = var.module_name
}

module "deployment_checker_lambda_function" {
  source = "../lambda_function"

  function_name     = "deployment-checker"
  lambda_source_dir = "${path.module}/../../../../src/lambdas/deployment_checker"
  handler           = "lambdas.deployment_checker.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.checker_lambda_timeout
  memory_size    = var.checker_lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  environment_variables = {
    LOG_LEVEL       = "INFO"
    REQUEST_TIMEOUT = "30"
    BITBUCKET_TOKEN = var.bitbucket_token
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
