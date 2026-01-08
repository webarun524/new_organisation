resource "aws_iam_role" "test_orchestrator" {
  name = "${var.resource_prefix}-test-orchestrator-sfn-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = local.merged_tags
}

resource "aws_iam_role_policy" "test_orchestrator_policy" {
  name = "${var.resource_prefix}-test-orchestrator-sfn-policy"
  role = aws_iam_role.test_orchestrator.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogDelivery",
          "logs:GetLogDelivery",
          "logs:UpdateLogDelivery",
          "logs:DeleteLogDelivery",
          "logs:ListLogDeliveries",
          "logs:PutResourcePolicy",
          "logs:DescribeResourcePolicies",
          "logs:DescribeLogGroups",
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          var.setup_lambda_arn,
          "${var.setup_lambda_arn}:*",
          var.checker_lambda_arn,
          "${var.checker_lambda_arn}:*",
          var.commit_collector_lambda_arn,
          "${var.commit_collector_lambda_arn}:*",
          var.config_composer_lambda_arn,
          "${var.config_composer_lambda_arn}:*",
          var.password_rotator_lambda_arn,
          "${var.password_rotator_lambda_arn}:*",
          var.reporter_lambda_arn,
          "${var.reporter_lambda_arn}:*",
          var.e2e_tests_role_arn,
          var.execution_record_lambda_arn,
          "${var.execution_record_lambda_arn}:*",
          var.dde_lambda_arn,
          "${var.dde_lambda_arn}:*",
          module.execution_params_validator_function.function_arn,
          "${module.execution_params_validator_function.function_arn}:*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "codebuild:StartBuild",
          "codebuild:StopBuild",
          "codebuild:BatchGetBuilds"
        ]
        Resource = [
          var.e2e_tests_project_arn
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "events:PutTargets",
          "events:PutRule",
          "events:DescribeRule"
        ],
        Resource = [
          "arn:aws:events:*:*:rule/StepFunctionsGetEventForCodeBuildStartBuildRule"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "states:StartExecution"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          aws_cloudwatch_log_group.test_orchestrator_logs.arn,
          "${aws_cloudwatch_log_group.test_orchestrator_logs.arn}:*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "events:RetrieveConnection",
          "events:RetrieveConnectionCredentials",
        ]
        Resource : [resource.aws_cloudwatch_event_connection.data_console.arn]
      },
      {
        Effect : "Allow",
        Action : [
          "secretsmanager:DescribeSecret",
          "secretsmanager:GetSecretValue",
        ],
        Resource : [resource.aws_cloudwatch_event_connection.data_console.secret_arn]
      },
      {
        Effect : "Allow",
        Action : [
          "states:InvokeHTTPEndpoint"
        ],
        Condition : {
          StringEquals : {
            "states:HTTPMethod" : "GET"
          },
          StringLike : {
            "states:HTTPEndpoint" : "https://*"
          }
        },
        Resource : "*"
      }
    ]
  })
}
