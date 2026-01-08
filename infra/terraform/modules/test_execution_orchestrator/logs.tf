resource "aws_cloudwatch_log_group" "test_orchestrator_logs" {
  name              = "${var.resource_prefix}-test-orchestrator"
  retention_in_days = 14
  tags              = local.merged_tags
}
