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

variable "backplane_account_id" {
  type        = string
  description = "AWS Account ID for Backplane resources"
  validation {
    condition     = can(regex("^[0-9]{12}$", var.backplane_account_id))
    error_message = "Must be a 12-digit AWS account ID."
  }
}

variable "approval_lambda_timeout" {
  description = "Lambda function timeout in seconds"
  default     = 60
  type        = number
}

variable "setup_trigger_lambda_timeout" {
  description = "Lambda function timeout in seconds"
  default     = 30
  type        = number
}

variable "commit_collector_lambda_timeout" {
  description = "Lambda function timeout in seconds"
  default     = 300
  type        = number
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  default     = 256
  type        = number
}

variable "bitbucket_token" {
  description = "Bitbucket API token for commit collector"
  type        = string
  sensitive   = true
}

variable "deployment_environment_code" {
  type        = string
  description = "Code representing the deployment environment"
  validation {
    condition     = can(regex("^(proto|proto2|proto3|dev|qa|preprod|utility|edi-qa|customer-prod)$", var.deployment_environment_code))
    error_message = "Must be one of the following: proto, proto2, proto3, dev, qa, preprod, utility, edi-qa, customer-prod."
  }
}

variable "e2e_tests_buildspec" {
  type        = string
  description = "Buildspec for the E2E tests"
  default     = "buildspecs/buildspec.yml"
}

#  bitbucket permission

variable "bitbucket_audience" {
  description = "The audience (client ID) from Bitbucket's OIDC configuration"
  type        = string
  sensitive   = true
}

variable "bitbucket_subjects" {
  description = "List of allowed Bitbucket subjects (workspace/repository patterns)"
  type        = list(string)
  default     = ["*"]

  validation {
    condition     = length(var.bitbucket_subjects) > 0
    error_message = "At least one Bitbucket subject must be specified."
  }
}

variable "bitbucket_thumbprint" {
  description = "The root CA thumbprint for Bitbucket's OIDC provider"
  type        = string
}
