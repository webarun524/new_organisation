module "execution_params_validator_function" {
  source = "../lambda_function"

  function_name     = local.function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/execution_params_validator"
  handler           = "lambdas.execution_params_validator.handler.lambda_handler"
  aws_region        = var.region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  environment_variables = {
    LOG_LEVEL       = "INFO"
    REQUEST_TIMEOUT = "20.0"
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
