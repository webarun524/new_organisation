locals {
  merged_tags = merge(var.tags, { Module = var.module_name })

  operations_portal_test_report_folder    = "operation_portal_subscription_test_reports"
  deployment_data_extractor_function_name = "deployment-data-extractor"
}
