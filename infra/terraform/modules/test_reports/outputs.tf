/* S3 */
output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.e2e_reports.bucket
}

output "s3_policy_arn" {
  description = "IAM policy ARN providing S3 access"
  value       = aws_iam_policy.e2e_s3_policy.arn
}

output "report_bucket_arn" {
  description = "ARN of the S3 bucket for E2E test reports."
  value       = aws_s3_bucket.e2e_reports.arn
}

output "report_bucket_id" {
  description = "ID of the S3 bucket for E2E test reports."
  value       = aws_s3_bucket.e2e_reports.id
}

output "report_bucket_folders" {
  description = "List of folder keys created in the reports bucket."
  value       = [for f in aws_s3_object.folders : f.key]
}

output "report_bucket_policy_id" {
  description = "ID of the bucket policy applied to the reports bucket."
  value       = aws_s3_bucket_policy.this.id
}


/* Reporter lambda */

output "reporter_lambda_function_name" {
  description = "Name of the reporter handler Lambda function"
  value       = module.lambda_reporter.function_name
}

output "reporter_lambda_function_arn" {
  description = "ARN of the reporter handler Lambda function"
  value       = module.lambda_reporter.function_arn
}

output "reporter_lambda_invoke_arn" {
  description = "Invoke ARN of the reporter handler Lambda function"
  value       = module.lambda_reporter.function_invoke_arn
}

output "reporter_lambda_iam_role_arn" {
  description = "IAM role ARN for the reporter handler Lambda function"
  value       = module.lambda_reporter.role_arn
}

output "reporter_lambda_log_group" {
  description = "CloudWatch Log Group for the reporter handler Lambda function"
  value       = module.lambda_reporter.log_group_name
}


/* SNS topic */

output "topic_arn" {
  description = "SNS Report topic ARN"
  value       = aws_sns_topic.report_topic.arn
}

output "topic_id" {
  description = "SNS Report topic ID"
  value       = aws_sns_topic.report_topic.id
}

output "topic_name" {
  description = "SNS Report topic name"
  value       = aws_sns_topic.report_topic.name
}
