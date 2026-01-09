locals {
  function_name = "commit-collector"
  merged_tags   = merge(var.tags, { Module = var.module_name })
}
