{
  "Trigger Environment Setup": {
    "Type": "Task",
    "Comment": "Trigger the setup of the testing environment",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${SetupLambdaName}",
      "Payload": {
        "environment": "${DeploymentEnvironment}",
        "bb_env_code.$": "$.ConfigComposeResult.Payload.body.bb_env_code",
        "target_branch_name.$": "$.BackplaneTargetBranchName"
      }
    },
    "ResultPath": "$.EnvTriggerResult",
    "Retry": [
      {
        "ErrorEquals": [ "Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException" ],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2
      }
    ],
    "Catch": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Env Trigger Error"
      }
    ],
    "Next": "Env Checker - Initialize Poll Counter"
  },

  "Enrich Env Trigger Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to trigger the Environment Setup Lambda.",
      "SourceState": "Trigger Environment Setup",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Env Checker - Initialize Poll Counter": {
    "Type": "Pass",
    "Result": { "poll_count": 0, "max_polls": 20 },
    "ResultPath": "$.PollInfo",
    "Next": "Env Checker - Check Environment Setup State"
  },

  "Env Checker - Check Environment Setup State": {
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${DeploymentCheckerLambdaName}",
      "Payload": { "execution_uuid.$": "$.EnvTriggerResult.Payload.body.pipelineID" }
    },
    "ResultPath": "$.DeploymentCheckerResult",
    "TimeoutSeconds": 1800,
    "Catch": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Env Checker Error"
      }
    ],
    "Next": "Env Checker - Check Completion Status"
  },

  "Enrich Env Checker Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "The Deployment Checker Lambda crashed or timed out.",
      "SourceState": "Env Checker - Check Environment Setup State",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Env Checker - Check Completion Status": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.DeploymentCheckerResult.Payload.body.is_completed",
        "BooleanEquals": true,
        "Next": "Collect Commit Hashes"
      }
    ],
    "Default": "Env Checker - Wait Before Next Poll"
  },

  "Env Checker - Wait Before Next Poll": {
    "Type": "Wait",
    "Seconds": 120,
    "Next": "Env Checker - Increment Poll Counter"
  },

  "Env Checker - Increment Poll Counter": {
    "Type": "Pass",
    "Parameters": {
      "poll_count.$": "States.MathAdd($.PollInfo.poll_count, 1)",
      "max_polls.$": "$.PollInfo.max_polls"
    },
    "ResultPath": "$.PollInfo",
    "Next": "Env Checker - Check Poll Limit"
  },

  "Env Checker - Check Poll Limit": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.PollInfo.poll_count",
        "NumericGreaterThanEqualsPath": "$.PollInfo.max_polls",
        "Next": "Enrich Env Polling Timeout"
      }
    ],
    "Default": "Env Checker - Check Environment Setup State"
  },

  "Enrich Env Polling Timeout": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Environment Setup did not complete within the allotted polling limit.",
      "SourceState": "Env Checker",
      "TechnicalError": "PollingLimitExceeded",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  }
}
