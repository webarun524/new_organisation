output "orchestrator_arn" {
  description = "ARN of the E2E Orchestration Step Function State Machine"
  value       = aws_sfn_state_machine.test_orchestrator.arn
}

output "orchestrator_name" {
  description = "Name of the E2E Orchestration Step Function State Machine"
  value       = aws_sfn_state_machine.test_orchestrator.name
}

output "orchestrator_definition" {
  description = "Definition of the E2E Orchestration Step Function State Machine"
  value       = aws_sfn_state_machine.test_orchestrator.definition
}

output "orchestrator_status" {
  description = "Status of the E2E Orchestration Step Function State Machine"
  value       = aws_sfn_state_machine.test_orchestrator.status
}

output "orchestrator_log_group_name" {
  description = "CloudWatch Log Group name for the E2E Orchestration Step Function"
  value       = aws_cloudwatch_log_group.test_orchestrator_logs.name
}

output "orchestrator_role_arn" {
  description = "IAM Role ARN for the E2E Orchestration Step Function"
  value       = aws_iam_role.test_orchestrator.arn
}

output "execution_params_validator_function_name" {
  description = "Name of the execution_params_validator Lambda function"
  value       = module.execution_params_validator_function.function_name
}

output "execution_params_validator_function_arn" {
  description = "ARN of the execution_params_validator Lambda function"
  value       = module.execution_params_validator_function.function_arn
}

output "execution_params_validator_invoke_arn" {
  description = "Invoke ARN of the execution_params_validator Lambda function"
  value       = module.execution_params_validator_function.function_invoke_arn
}

output "execution_params_validator_role_arn" {
  description = "IAM role ARN for the execution_params_validator Lambda function"
  value       = module.execution_params_validator_function.role_arn
}

output "execution_params_validator_log_group_name" {
  description = "CloudWatch Log Group name for the execution_params_validator Lambda function"
  value       = module.execution_params_validator_function.log_group_name
}
