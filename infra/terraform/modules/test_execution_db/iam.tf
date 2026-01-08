data "aws_iam_policy_document" "e2e_dynamodb_access" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:GetItem",
      "dynamodb:Query"
    ]
    resources = [
      aws_dynamodb_table.e2e_execution_record.arn,
      "${aws_dynamodb_table.e2e_execution_record.arn}/index/*"
    ]
  }
}

resource "aws_iam_policy" "e2e_dynamodb_policy" {
  name        = "${var.resource_prefix}-execution-record-dynamodb-policy"
  description = "Allows read/write access to the E2EExecutionRecord table"
  policy      = data.aws_iam_policy_document.e2e_dynamodb_access.json
  tags        = local.merged_tags
}
