data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_function_role" {
  name               = "${var.resource_prefix}-${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = local.merged_tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "lambda_access_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${var.aws_region}:*:log-group:${local.log_group_name}*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "sns:Publish"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_function_policy" {
  name        = "${var.resource_prefix}-${var.function_name}-lambda-function-policy"
  description = "Custom policy for ${var.resource_prefix} lambda function"
  policy      = data.aws_iam_policy_document.lambda_access_policy.json

  tags = local.merged_tags
}

resource "aws_iam_role_policy_attachment" "lambda_function_custom_policy" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = aws_iam_policy.lambda_function_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_additional_custom_policies" {
  for_each = { for idx, arn in var.extra_policy_arns : idx => arn }

  role       = aws_iam_role.lambda_function_role.name
  policy_arn = each.value
}
