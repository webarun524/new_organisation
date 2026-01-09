/* DynamoDB Table for E2E Execution Records */

resource "aws_dynamodb_table" "e2e_execution_record" {
  name         = local.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = local.hash_key_name

  server_side_encryption {
    enabled = true
  }

  attribute {
    name = local.hash_key_name
    type = "S"
  }

  attribute {
    name = "Status"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "S"
  }

  global_secondary_index {
    name            = local.secondary_index_name
    hash_key        = "Status"
    range_key       = "CreatedAt"
    projection_type = "ALL"
  }

  deletion_protection_enabled = false

  point_in_time_recovery {
    enabled = true
  }

  tags = local.merged_tags
}


/* DynamoDB Lambda Handler */

module "test_execution_record_handler_lambda_function" {
  source = "../lambda_function"

  function_name     = local.test_execution_record_handler_function_name
  lambda_source_dir = "${path.module}/../../../../src/lambdas/execution_record_handler"
  handler           = "lambdas.execution_record_handler.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  extra_policy_arns = [
    aws_iam_policy.e2e_dynamodb_policy.arn
  ]

  environment_variables = {
    LOG_LEVEL            = "INFO"
    REQUEST_TIMEOUT      = "20.0"
    REGION               = var.aws_region
    TABLE_NAME           = local.table_name
    HASH_KEY_NAME        = local.hash_key_name
    SECONDARY_INDEX_NAME = local.secondary_index_name
  }

  tags        = local.merged_tags
  module_name = var.module_name
}
