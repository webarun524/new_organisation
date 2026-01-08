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

variable "project_name" {
  type        = string
  description = "Name of the CodeBuild project"
}

variable "build_image" {
  type        = string
  description = "Docker image for the build environment"
  default     = "aws/codebuild/standard:5.0"
}

variable "build_compute_type" {
  type        = string
  description = "Compute type for the build"
  default     = "BUILD_GENERAL1_SMALL"
}

variable "environment_variables" {
  description = "Environment variables for the CodeBuild project"
  type = list(object({
    name  = string
    value = string
    type  = string
  }))
  default = []
}

variable "buildspec" {
  description = "Path to the buildspec file for the CodeBuild project."
  type        = string
  default     = "buildspecs/buildspec.yml"
}

variable "source_type" {
  description = "Type of the source repository"
  type        = string
  default     = "NO_SOURCE"
}

variable "source_location" {
  description = "Location of the source code for CodeBuild"
  type        = string
  default     = null
}

variable "artifacts_bucket" {
  description = "S3 bucket for CodeBuild artifacts"
  type        = string
  default     = null
}

variable "e2e_folder_path" {
  description = "Path to the e2e folder to be zipped and uploaded to S3"
  type        = string
  default     = "../../../../e2e"
}

variable "report_bucket_arn" {
  description = "ARN of s3 bucket for storing test reports"
  type        = string
}

variable "report_bucket_name" {
  type        = string
  description = "Name of the S3 bucket for storing test reports"
}

variable "execution_record_lambda_arn" {
  description = "ARN of lambda that updates dynamo report record"
  type        = string
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

variable "python_version" {
  type        = string
  description = "Python version"
}
