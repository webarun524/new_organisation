# Approval Handler Lambda Function
module "approval_handler_lambda_function" {
  source = "../lambda_function"

  function_name     = local.function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/approval_handler"
  handler           = "lambdas.approval_handler.handler.lambda_handler"
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
    REQUEST_TIMEOUT = "20.0"
    AUTHOR_EMAIL    = var.test_admin_email
  }

  tags        = local.merged_tags
  module_name = var.module_name
}

resource "aws_sns_topic_subscription" "approval_subscription" {
  topic_arn = local.external_sns_topic_arn
  protocol  = "lambda"
  endpoint  = module.approval_handler_lambda_function.function_arn
}

resource "aws_lambda_permission" "allow_sns_invoke" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = module.approval_handler_lambda_function.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.external_sns_topic_arn
}
