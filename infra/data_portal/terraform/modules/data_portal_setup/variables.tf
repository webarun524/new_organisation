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

variable "trusted_accounts" {
  type        = list(string)
  description = "List of AWS account IDs that can assume the role"
}

variable "organization_id" {
  type        = string
  description = "The AWS Organization ID for the organization"
}

variable "domain_name" {
  type        = string
  description = "The domain name for the E2E test suite Data Portal"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
}

variable "service_name" {
  type        = string
  description = "Name of the service"
}
