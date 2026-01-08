output "layer_arn" {
  description = "ARN of the Lambda layer (without version)"
  value       = aws_lambda_layer_version.shared_layer.layer_arn
}

output "layer_version_arn" {
  description = "ARN of the Lambda layer with version"
  value       = aws_lambda_layer_version.shared_layer.arn
}

output "layer_version" {
  description = "Version number of the Lambda layer"
  value       = aws_lambda_layer_version.shared_layer.version
}

output "layer_name" {
  description = "Name of the Lambda layer"
  value       = aws_lambda_layer_version.shared_layer.layer_name
}

output "layer_source_code_hash" {
  description = "Base64-encoded SHA256 hash of the layer ZIP"
  value       = aws_lambda_layer_version.shared_layer.source_code_hash
}

output "layer_compatible_runtimes" {
  description = "Compatible Python runtimes for the layer"
  value       = aws_lambda_layer_version.shared_layer.compatible_runtimes
}
