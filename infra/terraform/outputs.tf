/* Lambda Layer Outputs */

output "lambda_layer_arn" {
  description = "ARN of the Lambda layer (without version)"
  value       = module.lambda_layer.layer_arn
}

output "lambda_layer_version_arn" {
  description = "ARN of the Lambda layer with version"
  value       = module.lambda_layer.layer_version_arn
}

output "lambda_layer_version" {
  description = "Version number of the Lambda layer"
  value       = module.lambda_layer.layer_version
}

output "lambda_layer_name" {
  description = "Name of the Lambda layer"
  value       = module.lambda_layer.layer_name
}

output "lambda_layer_source_code_hash" {
  description = "Base64-encoded SHA256 hash of the layer ZIP"
  value       = module.lambda_layer.layer_source_code_hash
}

output "lambda_layer_compatible_runtimes" {
  description = "Compatible Python runtimes for the layer"
  value       = module.lambda_layer.layer_compatible_runtimes
}


/* Approval Handler Lambda Outputs */

output "approval_handler_function_name" {
  description = "Name of the approval handler Lambda function"
  value       = module.approval_handler.lambda_function_name
}

output "approval_handler_function_arn" {
  description = "ARN of the approval handler Lambda function"
  value       = module.approval_handler.lambda_function_arn
}

output "approval_handler_invoke_arn" {
  description = "Invoke ARN of the approval handler Lambda function"
  value       = module.approval_handler.lambda_invoke_arn
}

output "approval_handler_role_arn" {
  description = "IAM role ARN for the approval handler Lambda function"
  value       = module.approval_handler.iam_role_arn
}

output "approval_handler_log_group" {
  description = "CloudWatch Log Group for the approval handler Lambda function"
  value       = module.approval_handler.lambda_log_group
}


/* CodeBuild Module Outputs */

output "codebuild_project_name" {
  description = "Name of the CodeBuild project"
  value       = module.e2e_tests.project_name
}

output "codebuild_project_arn" {
  description = "ARN of the CodeBuild project"
  value       = module.e2e_tests.project_arn
}

output "codebuild_project_id" {
  description = "ID of the CodeBuild project"
  value       = module.e2e_tests.project_id
}

output "codebuild_role_arn" {
  description = "IAM role ARN used by CodeBuild"
  value       = module.e2e_tests.role_arn
}

output "codebuild_e2e_artifacts_bucket" {
  description = "S3 bucket name used by CodeBuild for e2e artifacts"
  value       = module.e2e_tests.e2e_artifacts_bucket
}

output "codebuild_dde_function_name" {
  description = "Name of the deployment data extractor Lambda function (from CodeBuild module)"
  value       = module.e2e_tests.dde_function_name
}

output "codebuild_dde_function_arn" {
  description = "ARN of the deployment data extractor Lambda function (from CodeBuild module)"
  value       = module.e2e_tests.dde_function_arn
}


/* Orchestrator Outputs */

output "test_orchestrator_arn" {
  description = "ARN of the Test Orchestrator Step Function State Machine"
  value       = module.test_execution_orchestrator.orchestrator_arn
}

output "test_orchestrator_name" {
  description = "Name of the Test Orchestrator Step Function State Machine"
  value       = module.test_execution_orchestrator.orchestrator_name
}

output "test_orchestrator_status" {
  description = "Status of the Test Orchestrator Step Function State Machine"
  value       = module.test_execution_orchestrator.orchestrator_status
}

output "test_orchestrator_log_group_name" {
  description = "CloudWatch Log Group name for the Test Orchestrator Step Function"
  value       = module.test_execution_orchestrator.orchestrator_log_group_name
}

output "test_orchestrator_role_arn" {
  description = "IAM Role ARN for the Test Orchestrator Step Function"
  value       = module.test_execution_orchestrator.orchestrator_role_arn
}

output "execution_params_validator_function_name" {
  description = "Name of the execution_params_validator Lambda function"
  value       = module.test_execution_orchestrator.execution_params_validator_function_name
}

output "execution_params_validator_function_arn" {
  description = "ARN of the execution_params_validator Lambda function"
  value       = module.test_execution_orchestrator.execution_params_validator_function_arn
}

output "execution_params_validator_invoke_arn" {
  description = "Invoke ARN of the execution_params_validator Lambda function"
  value       = module.test_execution_orchestrator.execution_params_validator_invoke_arn
}

output "execution_params_validator_role_arn" {
  description = "IAM role ARN for the execution_params_validator Lambda function"
  value       = module.test_execution_orchestrator.execution_params_validator_role_arn
}

output "execution_params_validator_log_group_name" {
  description = "CloudWatch Log Group name for the execution_params_validator Lambda function"
  value       = module.test_execution_orchestrator.execution_params_validator_log_group_name
}


/* Test Execution DB outputs */

output "test_execution_db_table_name" {
  description = "Name of the DynamoDB table for E2E execution records."
  value       = module.test_execution_db.table_name
}

output "test_execution_db_table_arn" {
  description = "ARN of the DynamoDB table for E2E execution records."
  value       = module.test_execution_db.table_arn
}

output "test_execution_db_table_id" {
  description = "ID of the DynamoDB table for E2E execution records."
  value       = module.test_execution_db.table_id
}

output "test_execution_db_table_stream_arn" {
  description = "Stream ARN of the DynamoDB table (if enabled)."
  value       = module.test_execution_db.table_stream_arn
}

output "test_execution_db_table_gsi_names" {
  description = "List of global secondary index names."
  value       = module.test_execution_db.table_gsi_names
}

output "terh_lambda_function_name" {
  description = "Name of the Lambda function for test execution record handler."
  value       = module.test_execution_db.terh_lambda_function_name
}

output "terh_lambda_function_arn" {
  description = "ARN of the Lambda function for test execution record handler."
  value       = module.test_execution_db.terh_lambda_function_arn
}

output "terh_lambda_function_role_arn" {
  description = "IAM Role ARN for the test execution record handler Lambda function."
  value       = module.test_execution_db.terh_lambda_function_role_arn
}


/* Commit collector */

output "commit_collector_function_name" {
  description = "Name of the commit collector Lambda function"
  value       = module.commit_collector.lambda_function_name
}

output "commit_collector_function_arn" {
  description = "ARN of the commit collector Lambda function"
  value       = module.commit_collector.lambda_function_arn
}

output "commit_collector_invoke_arn" {
  description = "Invoke ARN of the commit collector Lambda function"
  value       = module.commit_collector.lambda_invoke_arn
}

output "commit_collector_role_arn" {
  description = "IAM role ARN for the commit collector Lambda function"
  value       = module.commit_collector.iam_role_arn
}

output "commit_collector_log_group" {
  description = "CloudWatch Log Group for the commit collector Lambda function"
  value       = module.commit_collector.lambda_log_group
}

/* Test reports */

output "reporter_lambda_function_name" {
  description = "Name of the reporter handler Lambda function"
  value       = module.test_reports.reporter_lambda_function_name
}

output "reporter_lambda_function_arn" {
  description = "ARN of the reporter handler Lambda function"
  value       = module.test_reports.reporter_lambda_function_arn
}

output "reporter_lambda_invoke_arn" {
  description = "Invoke ARN of the reporter handler Lambda function"
  value       = module.test_reports.reporter_lambda_invoke_arn
}

output "reporter_lambda_role_arn" {
  description = "IAM role ARN for the reporter handler Lambda function"
  value       = module.test_reports.reporter_lambda_iam_role_arn
}

output "reporter_lambda_log_group" {
  description = "CloudWatch Log Group for the reporter handler Lambda function"
  value       = module.test_reports.reporter_lambda_log_group
}

output "report_topic_arn" {
  description = "SNS topic ARN for final reports"
  value       = module.test_reports.topic_arn
}

output "report_topic_name" {
  description = "SNS topic name for final reports"
  value       = module.test_reports.topic_name
}

# Setup lambda outputs

output "setup_lambda_function_name" {
  description = "Name of the setup trigger Lambda function"
  value       = module.environment_setup.setup_lambda_function_name
}

output "setup_lambda_function_arn" {
  description = "ARN of the setup trigger Lambda function"
  value       = module.environment_setup.setup_lambda_function_arn
}

output "setup_lambda_invoke_arn" {
  description = "Invoke ARN of the setup trigger Lambda function"
  value       = module.environment_setup.setup_lambda_invoke_arn
}

output "iam_role_arn" {
  description = "IAM role ARN for the setup trigger Lambda function"
  value       = module.environment_setup.iam_role_arn
}

output "setup_lambda_log_group" {
  description = "CloudWatch Log Group for the setup trigger Lambda function"
  value       = module.environment_setup.setup_lambda_log_group
}

# Deployment checker lambda outputs

output "deployment_checker_lambda_function_name" {
  description = "Name of the deployment checker Lambda function"
  value       = module.environment_setup.deployment_checker_lambda_function_name
}

output "deployment_checker_lambda_function_arn" {
  description = "ARN of the deployment checker Lambda function"
  value       = module.environment_setup.deployment_checker_lambda_function_arn
}

output "deployment_checker_lambda_invoke_arn" {
  description = "Invoke ARN of the deployment checker Lambda function"
  value       = module.environment_setup.deployment_checker_lambda_invoke_arn
}

output "deployment_checker_iam_role_arn" {
  description = "IAM role ARN for the deployment checker Lambda function"
  value       = module.environment_setup.deployment_checker_iam_role_arn
}

output "deployment_checker_lambda_log_group" {
  description = "CloudWatch Log Group for the deployment checker Lambda function"
  value       = module.environment_setup.deployment_checker_lambda_log_group
}

/* Config composer outputs */

output "config_composer_lambda_function_name" {
  description = "Name of the config composer Lambda function"
  value       = module.config_composer.lambda_function_name
}

output "config_composer_lambda_function_arn" {
  description = "ARN of the config composer Lambda function"
  value       = module.config_composer.lambda_function_arn
}

output "config_composer_lambda_function_invoke_arn" {
  description = "Invoke ARN of the config composer Lambda function"
  value       = module.config_composer.lambda_function_invoke_arn
}

output "config_composer_lambda_function_role_arn" {
  description = "IAM role ARN for the config composer Lambda function"
  value       = module.config_composer.lambda_function_role_arn
}

output "config_composer_lambda_log_group" {
  description = "CloudWatch Log Group for the config composer Lambda function"
  value       = module.config_composer.lambda_function_log_group
}

output "config_composer_admin_username_parameter_name" {
  description = "SSM parameter name for admin username produced by config composer"
  value       = module.config_composer.admin_username_parameter_name
}

output "config_composer_admin_username_parameter_arn" {
  description = "SSM parameter ARN for admin username produced by config composer"
  value       = module.config_composer.admin_username_parameter_arn
}

output "config_composer_operations_portal_url_parameter_name" {
  description = "SSM parameter name for operations portal URL produced by config composer"
  value       = module.config_composer.operations_portal_url_parameter_name
}

output "config_composer_operations_portal_url_parameter_arn" {
  description = "SSM parameter ARN for operations portal URL produced by config composer"
  value       = module.config_composer.operations_portal_url_parameter_arn
}

output "config_composer_admin_password_secret_name" {
  description = "Secrets Manager secret name for admin password produced by config composer"
  value       = module.config_composer.admin_password_secret_name
}

output "config_composer_admin_password_secret_arn" {
  description = "Secrets Manager secret ARN for admin password produced by config composer"
  value       = module.config_composer.admin_password_secret_arn
}

output "cc_password_rotator_function_name" {
  description = "Name of the password rotator Lambda function"
  value       = module.config_composer.password_rotator_function_name
}

output "cc_password_rotator_function_arn" {
  description = "ARN of the password rotator Lambda function"
  value       = module.config_composer.password_rotator_function_arn
}

output "cc_password_rotator_function_invoke_arn" {
  description = "Invoke ARN of the password rotator Lambda function"
  value       = module.config_composer.password_rotator_function_invoke_arn
}

output "cc_password_rotator_function_role_arn" {
  description = "IAM role ARN for the password rotator Lambda function"
  value       = module.config_composer.password_rotator_function_role_arn
}

output "cc_password_rotator_function_log_group" {
  description = "CloudWatch Log Group for the password rotator Lambda function"
  value       = module.config_composer.password_rotator_function_log_group
}


# bitbucket

output "bitbucket_config" {
  description = "Summary of Bitbucket Pipelines role configuration"
  value       = module.bitbucket_trigger_integration.bitbucket_role_configuration
}
