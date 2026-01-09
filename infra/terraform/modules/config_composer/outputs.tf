/* Lambda function outputs (forwarded from nested lambda module) */
output "lambda_function_name" {
  description = "Name of the config composer Lambda function"
  value       = module.config_composer_lambda_function.function_name
}

output "lambda_function_arn" {
  description = "ARN of the config composer Lambda function"
  value       = module.config_composer_lambda_function.function_arn
}

output "lambda_function_invoke_arn" {
  description = "Invoke ARN of the config composer Lambda function"
  value       = module.config_composer_lambda_function.function_invoke_arn
}

output "lambda_function_role_arn" {
  description = "IAM role ARN for the config composer Lambda function"
  value       = module.config_composer_lambda_function.role_arn
}

output "lambda_function_log_group" {
  description = "CloudWatch Log Group for the config composer Lambda function"
  value       = module.config_composer_lambda_function.log_group_name
}

/* SSM parameters (names and ARNs) */
output "admin_username_parameter_name" {
  description = "SSM parameter name for admin username"
  value       = aws_ssm_parameter.test_admin_user_name.name
}

output "admin_username_parameter_arn" {
  description = "SSM parameter ARN for admin username"
  value       = aws_ssm_parameter.test_admin_user_name.arn
}

output "admin_username_parameter_value" {
  description = "SSM parameter ARN for admin username"
  value       = aws_ssm_parameter.test_admin_user_name.value
}

output "operations_portal_url_parameter_name" {
  description = "SSM parameter name for operations portal URL"
  value       = aws_ssm_parameter.test_operations_portal_url.name
}

output "operations_portal_url_parameter_arn" {
  description = "SSM parameter ARN for operations portal URL"
  value       = aws_ssm_parameter.test_operations_portal_url.arn
}

output "test_inbox_address_parameter_name" {
  description = "SSM parameter name for inbox address"
  value       = aws_ssm_parameter.test_inbox_address.name
}

output "test_inbox_address_parameter_arn" {
  description = "SSM parameter ARN for inbox address"
  value       = aws_ssm_parameter.test_inbox_address.arn
}

/* Secrets (names and ARNs) */
output "admin_password_secret_name" {
  description = "Secrets Manager secret name for admin password"
  value       = aws_secretsmanager_secret.test_admin_user_password.name
}

output "admin_password_secret_arn" {
  description = "Secrets Manager secret ARN for admin password"
  value       = aws_secretsmanager_secret.test_admin_user_password.arn
}

output "inbox_password_secret_name" {
  description = "Secrets Manager secret name for inbox password"
  value       = aws_secretsmanager_secret.test_inbox_password.name
}

output "inbox_password_secret_arn" {
  description = "Secrets Manager secret ARN for inbox password"
  value       = aws_secretsmanager_secret.test_inbox_password.arn
}

/* Password rotator */

output "password_rotator_function_name" {
  description = "Name of the password rotator Lambda function"
  value       = module.dp_password_rotator_lambda_function.function_name
}

output "password_rotator_function_arn" {
  description = "ARN of the password rotator Lambda function"
  value       = module.dp_password_rotator_lambda_function.function_arn
}

output "password_rotator_function_invoke_arn" {
  description = "Invoke ARN of the password rotator Lambda function"
  value       = module.dp_password_rotator_lambda_function.function_invoke_arn
}

output "password_rotator_function_role_arn" {
  description = "IAM role ARN for the password rotator Lambda function"
  value       = module.dp_password_rotator_lambda_function.role_arn
}

output "password_rotator_function_log_group" {
  description = "CloudWatch Log Group for the password rotator Lambda function"
  value       = module.dp_password_rotator_lambda_function.log_group_name
}
