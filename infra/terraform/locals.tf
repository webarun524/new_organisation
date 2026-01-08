locals {
  resource_prefix = format("%s", var.service_name)
  python_version  = trim(file("${path.root}/../../.python-version"), "\n")

  tags = {
    Project   = var.service_name
    ManagedBy = "Terraform"
  }
}
