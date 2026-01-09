locals {
  function_name          = "approval-handler"
  merged_tags            = merge(var.tags, { Module = var.module_name })
  external_sns_topic_arn = "arn:aws:sns:${var.aws_region}:${var.backplane_account_id}:rps_approval_email_sns_topic"
}
