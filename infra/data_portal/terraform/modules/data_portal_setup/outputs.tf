output "custom_fulfillment_role_arn" {
  value       = aws_iam_role.custom_fulfillment_role.arn
  description = "ARN of the custom fulfillment IAM role"
}

output "custom_fulfillment_policy_arn" {
  value       = aws_iam_policy.custom_fulfillment_policy.arn
  description = "ARN of the custom fulfillment IAM policy"
}

output "route53_hosted_zone_id" {
  value       = aws_route53_zone.public_hz.zone_id
  description = "ID of the new hosted zone"
}

output "route53_ns_records" {
  value       = aws_route53_zone.public_hz.name_servers
  description = "Nameserver (NS) records for the new hosted zone"
}

output "route53_domain_name" {
  value       = aws_route53_zone.public_hz.name
  description = "Domain name of the hosted zone created"
}

output "cognito_secrets_ssm_cross_policy_arn" {
  value       = aws_iam_policy.cognito_secrets_ssm_cross_policy.arn
  description = "ARN of the Cognito secrets SSM cross IAM policy"
}

output "cognito_secrets_ssm_cross_role_arn" {
  value       = aws_iam_role.cognito_secrets_ssm_cross_role.arn
  description = "ARN of the Cognito secrets SSM cross IAM role"
}

output "dp_password_secret_name" {
  description = "Secrets Manager secret name for dp password"
  value       = aws_secretsmanager_secret.dp_password.name
}

output "dp_password_secret_arn" {
  description = "Secrets Manager secret ARN for dp password"
  value       = aws_secretsmanager_secret.dp_password.arn
}
