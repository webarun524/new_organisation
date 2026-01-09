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

variable "service_name" {
  type        = string
  description = "Name of the service"
  default     = "edi-e2e-tests"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
  default     = "us-east-1"
  validation {
    condition     = can(regex("^(us|af|ap|ca|cn|eu|il|me|sa)(-[a-z]+)+-[0-9]+$", var.aws_region))
    error_message = "Must be a valid AWS region name (e.g., us-east-1, eu-west-2, ap-southeast-3)."
  }
}
