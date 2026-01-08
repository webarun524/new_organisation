locals {
  merged_tags        = merge(var.tags, { Module = var.module_name })
  report_bucket_name = "dataops-e2e-reports"
  folder_names = [
    "operation_portal_subscription_test_reports/",
    "data_portal_verification_test_reports/",
    "data_portal_teardown_test_reports/",
    "final_reports/"
  ]
  topic_name = "report-topic"
}
