locals {
  merged_tags = merge(var.tags, { Module = var.module_name })
}
