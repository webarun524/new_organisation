resource "aws_sfn_state_machine" "test_orchestrator" {
  name     = "${var.resource_prefix}-test-orchestrator-sfn"
  role_arn = aws_iam_role.test_orchestrator.arn

  definition = jsonencode({
    Comment = "E2E Tests Orchestration with Parameter Validation"
    StartAt = "Validate Input"
    States  = local.e2e_main_definition.States
  })

  logging_configuration {
    level                  = "ALL"
    include_execution_data = true
    log_destination        = "${aws_cloudwatch_log_group.test_orchestrator_logs.arn}:*"
  }

  tracing_configuration {
    enabled = true
  }

  tags = local.merged_tags
}
