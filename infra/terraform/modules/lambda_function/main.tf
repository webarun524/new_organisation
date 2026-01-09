# Build Lambda function package
resource "null_resource" "build_lambda" {
  triggers = {
    # Rebuild when handler code changes
    handler_hash = sha256(join("", [
      for f in fileset(var.lambda_source_dir, "**/*.py") :
      filesha256("${var.lambda_source_dir}/${f}")
    ]))
    # Rebuild when build script changes
    build_script_hash = filesha256(var.build_script_path)
  }

  provisioner "local-exec" {
    command     = "${var.build_script_path} ${replace(var.function_name, "-", "_")}"
    working_dir = "${path.module}/../.."
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = local.log_group_name
  retention_in_days = var.log_retention_days

  tags = local.merged_tags
}

resource "aws_lambda_function" "lambda" {
  filename         = "${path.module}/../../build/layer_build/${replace(var.function_name, "-", "_")}.zip"
  function_name    = "${var.resource_prefix}-${var.function_name}"
  role             = aws_iam_role.lambda_function_role.arn
  handler          = var.handler
  source_code_hash = null_resource.build_lambda.id
  runtime          = "python${var.python_version}"
  timeout          = var.timeout
  memory_size      = var.memory_size

  layers = var.lambda_layers

  dynamic "environment" {
    for_each = length(var.environment_variables) > 0 ? [1] : []
    content {
      variables = var.environment_variables
    }
  }

  depends_on = [
    null_resource.build_lambda,
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_basic_execution,
  ]

  tags = local.merged_tags
}
