output "lambda_function_name" {
  description = "Name of the approval handler Lambda function"
  value       = module.commit_collector_lambda_function.function_name
}

output "lambda_function_arn" {
  description = "ARN of the approval handler Lambda function"
  value       = module.commit_collector_lambda_function.function_arn
}

output "lambda_invoke_arn" {
  description = "Invoke ARN of the approval handler Lambda function"
  value       = module.commit_collector_lambda_function.function_invoke_arn
}

output "iam_role_arn" {
  description = "IAM role ARN for the approval handler Lambda function"
  value       = module.commit_collector_lambda_function.role_arn
}

output "lambda_log_group" {
  description = "CloudWatch Log Group for the approval handler Lambda function"
  value       = module.commit_collector_lambda_function.log_group_name
}
