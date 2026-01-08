module "commit_collector_lambda_function" {
  source = "../lambda_function"

  function_name     = local.function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/commit_collector"
  handler           = "lambdas.commit_collector.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  environment_variables = {
    LOG_LEVEL       = "INFO"
    REQUEST_TIMEOUT = "140"
    BITBUCKET_TOKEN = var.bitbucket_token
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
