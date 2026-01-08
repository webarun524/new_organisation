# Setup lambda outputs

output "setup_lambda_function_name" {
  description = "Name of the setup trigger Lambda function"
  value       = module.setup_trigger_lambda_function.function_name
}

output "setup_lambda_function_arn" {
  description = "ARN of the setup trigger Lambda function"
  value       = module.setup_trigger_lambda_function.function_arn
}

output "setup_lambda_invoke_arn" {
  description = "Invoke ARN of the setup trigger Lambda function"
  value       = module.setup_trigger_lambda_function.function_invoke_arn
}

output "iam_role_arn" {
  description = "IAM role ARN for the setup trigger Lambda function"
  value       = module.setup_trigger_lambda_function.role_arn
}

output "setup_lambda_log_group" {
  description = "CloudWatch Log Group for the setup trigger Lambda function"
  value       = module.setup_trigger_lambda_function.log_group_name
}

# Deployment checker lambda outputs

output "deployment_checker_lambda_function_name" {
  description = "Name of the deployment checker Lambda function"
  value       = module.deployment_checker_lambda_function.function_name
}

output "deployment_checker_lambda_function_arn" {
  description = "ARN of the deployment checker Lambda function"
  value       = module.deployment_checker_lambda_function.function_arn
}

output "deployment_checker_lambda_invoke_arn" {
  description = "Invoke ARN of the deployment checker Lambda function"
  value       = module.deployment_checker_lambda_function.function_invoke_arn
}

output "deployment_checker_iam_role_arn" {
  description = "IAM role ARN for the deployment checker Lambda function"
  value       = module.deployment_checker_lambda_function.role_arn
}

output "deployment_checker_lambda_log_group" {
  description = "CloudWatch Log Group for the deployment checker Lambda function"
  value       = module.deployment_checker_lambda_function.log_group_name
}
