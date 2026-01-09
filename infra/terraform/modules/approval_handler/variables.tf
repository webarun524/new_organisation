variable "tags" {
  type        = map(string)
  description = "Tags to apply to resources"
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to apply to resource names"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
}

variable "module_name" {
  type        = string
  description = "Name of the module"
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

variable "backplane_account_id" {
  description = "AWS Account ID for Backplane resources"
  type        = string
}

variable "lambda_layer_arn" {
  type        = string
  description = "ARN of the Lambda layer to use"
}

variable "python_version" {
  type        = string
  description = "Python version"
}

variable "test_admin_email" {
  type        = string
  description = "Test Admin email value for message filtering"
}
