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

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
}

variable "lambda_layer_arn" {
  type        = string
  description = "ARN of the Lambda layer to use"
}

variable "python_version" {
  type        = string
  description = "Python version"
}

variable "execution_record_lambda_name" {
  type        = string
  description = "Execution record (update dynamoDB record) lambda name"
}

variable "execution_record_lambda_arn" {
  type        = string
  description = "Execution record (update dynamoDB record) lambda arn"
}
