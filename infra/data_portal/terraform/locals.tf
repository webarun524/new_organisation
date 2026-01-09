locals {
  resource_prefix = format("%s", var.service_name)
  tags = {
    Project   = var.service_name
    ManagedBy = "Terraform"
  }
}
