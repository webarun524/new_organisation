module "deployment_data_extractor_lambda_function" {
  source = "../lambda_function"

  function_name     = local.deployment_data_extractor_function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/deployment_data_extractor"
  handler           = "lambdas.deployment_data_extractor.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]
  extra_policy_arns = [
    aws_iam_policy.deployment_data_extractor_policy.arn
  ]

  environment_variables = {
    LOG_LEVEL           = "INFO"
    REQUEST_TIMEOUT     = "20.0"
    REPORTS_BUCKET_NAME = var.report_bucket_name
    REPORTS_FOLDER_NAME = local.operations_portal_test_report_folder
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
