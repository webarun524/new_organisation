/* Reporter resources */

data "aws_iam_policy_document" "e2e_s3_access" {
  statement {
    sid    = "S3AccessForE2EReports"
    effect = "Allow"

    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation",
      "s3:GetBucketVersioning",
      "s3:GetEncryptionConfiguration",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]

    resources = [
      aws_s3_bucket.e2e_reports.arn,
      "${aws_s3_bucket.e2e_reports.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "e2e_s3_policy" {
  name        = "${var.resource_prefix}-reports-s3-access-policy"
  description = "Allows read/write and metadata access to the ${local.report_bucket_name} S3 bucket"
  policy      = data.aws_iam_policy_document.e2e_s3_access.json
  tags        = local.merged_tags
}


/* Reporter resources */

resource "aws_iam_role" "sns_to_ses" {
  name = "${var.resource_prefix}-reports-sns-to-ses-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sns.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = local.merged_tags
}

resource "aws_iam_role_policy" "sns_ses_publish" {
  name = "${var.resource_prefix}-reports-sns-ses-publish-policy"
  role = aws_iam_role.sns_to_ses.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = aws_sns_topic.report_topic.arn
      }
    ]
  })
}

resource "aws_sns_topic_policy" "report_policy" {
  arn = aws_sns_topic.report_topic.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowPublishFromLambda"
        Effect = "Allow"
        Principal = {
          AWS = module.lambda_reporter.role_arn
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.report_topic.arn
      },
    ]
  })
}

data "aws_iam_policy_document" "invoke_record_lambda" {
  statement {
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [
      var.execution_record_lambda_arn,
      "${var.execution_record_lambda_arn}:*",
    ]
  }
}

resource "aws_iam_policy" "execute_record_lambda" {
  name        = "${var.resource_prefix}-invoke_record_lambda-policy"
  description = "Allows read/write access to the E2EExecutionRecord table"
  policy      = data.aws_iam_policy_document.invoke_record_lambda.json
  tags        = local.merged_tags
}
