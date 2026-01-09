locals {
  merged_tags    = merge(var.tags, { Module = var.module_name })
  log_group_name = "${var.resource_prefix}-${var.function_name}-lambda"
}
