/* S3 resources */

# Create S3 bucket
resource "aws_s3_bucket" "e2e_reports" {
  bucket = local.report_bucket_name
  tags   = local.merged_tags
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.e2e_reports.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.e2e_reports.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Create Folders
resource "aws_s3_object" "folders" {
  for_each = toset(local.folder_names)
  bucket   = aws_s3_bucket.e2e_reports.bucket
  key      = each.value
}

# Optional Bucket Policy
resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.e2e_reports.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}

data "aws_caller_identity" "current" {}
data "aws_iam_policy_document" "bucket_policy" {
  statement {
    sid    = "AllowTerraformStateAccess"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.e2e_reports.bucket}",
      "arn:aws:s3:::${aws_s3_bucket.e2e_reports.bucket}/*"
    ]
  }
}

# allow public policy application
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.e2e_reports.id

  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = true
}


/* Reporter resources */

resource "aws_sns_topic" "report_topic" {
  name         = "${var.resource_prefix}-${local.topic_name}"
  display_name = "Final e2e test report topic"
  tags         = local.merged_tags
}

module "lambda_reporter" {
  source = "../lambda_function"

  function_name     = "reporter"
  lambda_source_dir = "${path.module}/../../../../src/lambdas/reporter"
  handler           = "lambdas.reporter.handler.lambda_handler"
  aws_region        = var.aws_region
  resource_prefix   = var.resource_prefix

  python_version = var.python_version
  timeout        = var.lambda_timeout
  memory_size    = var.lambda_memory_size

  lambda_layers = [
    var.lambda_layer_arn
  ]

  extra_policy_arns = [
    aws_iam_policy.e2e_s3_policy.arn,
    aws_iam_policy.execute_record_lambda.arn,
  ]

  environment_variables = {
    LOG_LEVEL                    = "INFO"
    REQUEST_TIMEOUT              = "140"
    E2E_FINAL_REPORT_TOPIC_ARN   = aws_sns_topic.report_topic.arn
    EXECUTION_RECORD_LAMBDA_NAME = var.execution_record_lambda_name
    S3_REPORT_BUCKET             = aws_s3_bucket.e2e_reports.id
  }

  tags        = local.merged_tags
  module_name = "reporter-lambda-function"
}
