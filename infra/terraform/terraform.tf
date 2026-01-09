terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }
  required_version = ">= 1.13"

  backend "s3" {
    key = "edi-e2e-tests/terraform.tfstate"
  }
}
