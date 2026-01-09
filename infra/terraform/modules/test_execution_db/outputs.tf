output "table_name" {
  description = "Name of the DynamoDB table for E2E execution records."
  value       = aws_dynamodb_table.e2e_execution_record.name
}

output "table_arn" {
  description = "ARN of the DynamoDB table for E2E execution records."
  value       = aws_dynamodb_table.e2e_execution_record.arn
}

output "table_id" {
  description = "ID of the DynamoDB table for E2E execution records."
  value       = aws_dynamodb_table.e2e_execution_record.id
}

output "table_stream_arn" {
  description = "Stream ARN of the DynamoDB table (if enabled)."
  value       = aws_dynamodb_table.e2e_execution_record.stream_arn
}

output "table_gsi_names" {
  description = "List of global secondary index names."
  value       = [for gsi in aws_dynamodb_table.e2e_execution_record.global_secondary_index : gsi.name]
}

output "terh_lambda_function_name" {
  description = "Name of the Lambda function for test execution record handler."
  value       = module.test_execution_record_handler_lambda_function.function_name
}

output "terh_lambda_function_arn" {
  description = "ARN of the Lambda function for test execution record handler."
  value       = module.test_execution_record_handler_lambda_function.function_arn
}

output "terh_lambda_function_role_arn" {
  description = "IAM Role ARN for the test execution record handler Lambda function."
  value       = module.test_execution_record_handler_lambda_function.role_arn
}
