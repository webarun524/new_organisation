# Data Portal Terraform

This directory contains Terraform configuration that provisions the Data Portal helper resources required by the E2E test suite. It wraps a small module (`modules/data_portal_setup`) which creates DNS resources and an IAM role/policy used for custom fulfillment operations.

**Location:** `infra/data_portal/terraform`

## Prerequisites

- Terraform >= 1.13
- AWS CLI configured with appropriate credentials

## What this stack provides

- An IAM role and policy used by the Data Portal's custom fulfillment logic
- A Route53 hosted zone (public) for the test Data Portal domain
- NS records to delegate the hosted zone from your registrar

These resources are created by the `data_portal_setup` module (see `modules/data_portal_setup`).

## Usage

1. Initialize Terraform in this folder:

```bash
cd infra/data_portal/terraform
terraform init
```

2. Preview changes and apply:

```bash
terraform plan -out plan.tfplan
terraform apply plan.tfplan
```

3. After apply, use `terraform output` to inspect the outputs described below.

## Module wiring

This root folder calls the local module:

```hcl
module "data_portal_setup" {
	source           = "./modules/data_portal_setup"
	resource_prefix  = local.resource_prefix
	module_name      = "data-portal-setup"
	tags             = local.tags
	trusted_accounts = var.trusted_accounts
	domain_name      = var.domain_name
}
```

## Outputs

The root outputs re-expose module outputs for convenience (available after `terraform apply`):

- `data_portal_custom_fulfillment_role_arn`: ARN of the IAM role created for custom fulfillment.
- `data_portal_custom_fulfillment_policy_arn`: ARN of the IAM policy attached to the custom fulfillment role.
- `data_portal_route53_hosted_zone_id`: Route53 hosted zone ID created for the Data Portal domain.
- `data_portal_route53_ns_records`: Nameserver (NS) records for the hosted zone (use these at your registrar).

Example:

```bash
terraform output data_portal_route53_ns_records
```

## Post-deploy / manual steps

- If this is a new hosted zone, update your domain registrar to delegate to the NS servers printed by `data_portal_route53_ns_records`.
- Verify DNS propagation (e.g., `dig NS <your-domain>`).

## Troubleshooting

- Hosted zone not resolving: ensure NS records were added at the registrar and allow time for propagation.
- Permissions: if downstream services require access to the custom fulfillment role, ensure the correct trust relationships and IAM policies are configured.

## Notes

- The module creates resources under `modules/data_portal_setup`. If you need to change secret names, DNS names, or trust accounts, edit that module and re-run `terraform plan`.
- Keep sensitive values out of Terraform source — update any generated secrets in the AWS Console or via the AWS CLI after apply if the module creates placeholder secret values.

---

If you want, I can also add a short example showing how to read the outputs from a CI/CD pipeline or add a verified-records script to check DNS propagation automatically.
