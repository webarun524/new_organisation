terraform {
  required_version = ">= 1.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}
