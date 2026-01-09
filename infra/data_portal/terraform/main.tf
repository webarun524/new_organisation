module "data_portal_setup" {
  source           = "./modules/data_portal_setup"
  resource_prefix  = local.resource_prefix
  module_name      = "data-portal-setup"
  tags             = local.tags
  trusted_accounts = var.trusted_accounts
  domain_name      = var.domain_name
  organization_id  = var.organization_id
  aws_region       = var.aws_region
  service_name     = var.service_name
}
