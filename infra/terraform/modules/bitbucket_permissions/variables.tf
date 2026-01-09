variable "sfn_orchestrator_arn" {
  type        = string
  description = "arn of E2E Step Function Orchestrator"
}

variable "bitbucket_audience" {
  description = "The audience (client ID) from Bitbucket's OIDC configuration"
  type        = string
  sensitive   = true
}

variable "bitbucket_subjects" {
  description = "List of allowed Bitbucket subjects (workspace/repository patterns)"
  type        = list(string)

  validation {
    condition     = length(var.bitbucket_subjects) > 0
    error_message = "At least one Bitbucket subject must be specified."
  }
}

variable "bitbucket_oidc_provider_url" {
  description = "The Bitbucket OpenID Connect provider URL"
  type        = string
}

variable "bitbucket_thumbprint" {
  description = "The root CA thumbprint for Bitbucket's OIDC provider"
  type        = string
}

variable "max_session_duration" {
  description = "Maximum session duration in seconds for the role"
  type        = number
  # 1h
  default = 3600
  validation {
    condition     = var.max_session_duration >= 3600 && var.max_session_duration <= 43200
    error_message = "Session duration must be between 900 (15 minutes) and 43200 (12 hours) seconds."
  }
}

variable "resource_prefix" {
  type        = string
  description = "Prefix to apply to resource names"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to resources"
}

variable "module_name" {
  type        = string
  description = "Name of the module"
}
