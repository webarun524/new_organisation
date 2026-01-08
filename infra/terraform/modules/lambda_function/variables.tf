# Required variables
variable "function_name" {
  description = "Name of the Lambda function (e.g., 'approval_handler', 'commit_collector')"
  type        = string
}

variable "lambda_source_dir" {
  description = "Path to the Lambda function source directory relative to infra module (e.g., '../src/lambdas/approval_handler')"
  type        = string
}

variable "handler" {
  description = "Lambda handler path (e.g., 'lambdas.approval_handler.handler.lambda_handler')"
  type        = string
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to apply to resource names"
}

variable "python_version" {
  description = "Python version"
  type        = string
}

variable "module_name" {
  type        = string
  description = "Name of the module"
}


# Optional variables with defaults
variable "timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 60
}

variable "memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 256
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}

variable "environment_variables" {
  description = "Environment variables for the Lambda function"
  type        = map(string)
  default     = {}
}

variable "lambda_layers" {
  description = "List of Lambda layer ARNs to attach"
  type        = list(string)
  default     = []
}

variable "build_script_path" {
  description = "Path to the build script relative to the infra directory"
  type        = string
  default     = "./modules/lambda_layer/build_lambda.sh"
}

variable "extra_policy_arns" {
  description = "Additional IAM policy ARNs to attach to the Lambda Role"
  type        = list(string)
  default     = []
}
