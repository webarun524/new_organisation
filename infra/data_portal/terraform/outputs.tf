output "data_portal_custom_fulfillment_role_arn" {
  description = "ARN of the custom fulfillment IAM role created by the data_portal_setup module"
  value       = module.data_portal_setup.custom_fulfillment_role_arn
}

output "data_portal_custom_fulfillment_policy_arn" {
  description = "ARN of the custom fulfillment IAM policy created by the data_portal_setup module"
  value       = module.data_portal_setup.custom_fulfillment_policy_arn
}

output "data_portal_route53_hosted_zone_id" {
  description = "ID of the hosted zone created by the data_portal_setup module"
  value       = module.data_portal_setup.route53_hosted_zone_id
}

output "data_portal_route53_ns_records" {
  description = "Nameserver (NS) records for the hosted zone created by the data_portal_setup module"
  value       = module.data_portal_setup.route53_ns_records
}

output "data_portal_route53_domain_name" {
  description = "Domain name of the hosted zone created by the data_portal_setup module"
  value       = module.data_portal_setup.route53_domain_name
}

output "data_portal_cognito_secrets_ssm_cross_policy_arn" {
  description = "ARN of the Cognito secrets SSM cross IAM policy created by the data_portal_setup module"
  value       = module.data_portal_setup.cognito_secrets_ssm_cross_policy_arn
}

output "data_portal_cognito_secrets_ssm_cross_role_arn" {
  description = "ARN of the Cognito secrets SSM cross IAM role created by the data_portal_setup module"
  value       = module.data_portal_setup.cognito_secrets_ssm_cross_role_arn
}

output "dp_password_secret_name" {
  description = "Secrets Manager secret name for dp password"
  value       = module.data_portal_setup.dp_password_secret_name
}

output "dp_password_secret_arn" {
  description = "Secrets Manager secret ARN for dp password"
  value       = module.data_portal_setup.dp_password_secret_arn
}
