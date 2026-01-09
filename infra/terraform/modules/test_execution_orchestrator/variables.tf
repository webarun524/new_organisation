variable "tags" {
  type        = map(string)
  description = "Tags to apply to resources"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to apply to resource names"
}

variable "module_name" {
  type        = string
  description = "Name of the module"
}

variable "setup_lambda_name" {
  type        = string
  description = "Name of the lambda that triggers dataops-deployments deployment pipeline"
}

variable "setup_lambda_arn" {
  type        = string
  description = "ARN of the lambda that triggers dataops-deployments deployment pipeline"
}

variable "checker_lambda_name" {
  type        = string
  description = "Name of the lambda that checks status of dataops-deployments deployment pipeline"
}

variable "checker_lambda_arn" {
  type        = string
  description = "ARN of the lambda that  checks status of dataops-deployments deployment pipeline"
}

variable "commit_collector_lambda_name" {
  type        = string
  description = "Name of the lambda that collects deployed commit hashes to the environment"
}

variable "commit_collector_lambda_arn" {
  type        = string
  description = "ARN of the lambda that  collects deployed commit hashes to the environment"
}

variable "deployment_environment_code" {
  type        = string
  description = "Code representing the deployment environment"
}

variable "config_composer_lambda_arn" {
  type        = string
  description = "ARN of the config composer lambda function"
}

variable "config_composer_lambda_name" {
  type        = string
  description = "Name of the config composer lambda function"
}

variable "password_rotator_lambda_arn" {
  type        = string
  description = "ARN of the password rotator lambda function"
}

variable "password_rotator_lambda_name" {
  type        = string
  description = "Name of the password rotator lambda function"
}

variable "e2e_tests_project_arn" {
  type        = string
  description = "ARN of the codebuild project to run e2e tests"
}

variable "e2e_tests_project_name" {
  type        = string
  description = "Name of the codebuild project to run e2e tests"
}

variable "e2e_tests_role_arn" {
  type        = string
  description = "ARN of the IAM role for codebuild to run e2e tests"
}

variable "region" {
  type        = string
  description = "AWS region where resources are deployed"
}

variable "reporter_lambda_name" {
  type        = string
  description = "Name of the lambda that handles final report"
}

variable "reporter_lambda_arn" {
  type        = string
  description = "ARN of the lambda that handles final report"
}

variable "execution_record_lambda_name" {
  type        = string
  description = "Name of the lambda that initializes E2E DB record"
}

variable "execution_record_lambda_arn" {
  type        = string
  description = "ARN of the lambda that initializes E2E DB record"
}

variable "dde_lambda_name" {
  type        = string
  description = "Name of the Deployment Data Extractor lambda"
}

variable "dde_lambda_arn" {
  type        = string
  description = "ARN of the Deployment Data Extractor lambda"
}

variable "python_version" {
  type        = string
  description = "Python version"
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  default     = 60
  type        = number
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  default     = 256
  type        = number
}

variable "lambda_layer_arn" {
  type        = string
  description = "ARN of the Lambda layer to use"
}
