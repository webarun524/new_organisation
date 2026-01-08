output "project_name" {
  description = "The name of the CodeBuild project"
  value       = aws_codebuild_project.this.name
}

output "project_arn" {
  description = "The ARN of the CodeBuild project"
  value       = aws_codebuild_project.this.arn
}

output "project_id" {
  description = "The ID of the CodeBuild project"
  value       = aws_codebuild_project.this.id
}

output "role_arn" {
  description = "The ARN of the IAM role for the CodeBuild project"
  value       = aws_iam_role.codebuild_role.arn
}

output "e2e_artifacts_bucket" {
  description = "The name of the S3 bucket for e2e artifacts"
  value       = aws_s3_bucket.e2e_artifacts.bucket
}

output "dde_function_name" {
  description = "Name of the deployment data extractor Lambda function"
  value       = module.deployment_data_extractor_lambda_function.function_name
}

output "dde_function_arn" {
  description = "ARN of the deployment data extractor Lambda function"
  value       = module.deployment_data_extractor_lambda_function.function_arn
}
