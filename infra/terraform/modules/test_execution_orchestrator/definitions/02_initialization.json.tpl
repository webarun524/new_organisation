{
  "Initialize E2E DB Record": {
    "Type": "Task",
    "Comment": "Initialize database record for tracking workflow progress",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${ExecutionRecordLambdaName}",
      "Payload": { "Status": "initialized" }
    },
    "ResultPath": "$.DbInitResult",
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
        "Next": "Enrich DB Init Error"
      }
    ],
    "Next": "Check Update E2E DB Record - Initialize E2E DB Record"
  },

  "Check Update E2E DB Record - Initialize E2E DB Record": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.DbInitResult.Payload.statusCode",
        "NumericEquals": 200,
        "Next": "Compose Config"
      }
    ],
    "Default": "Enrich DB Init Error"
  },

  "Enrich DB Init Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to initialize the E2E Database Record.",
      "SourceState": "Initialize E2E DB Record",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId": null
    },
    "ResultPath": "$.GlobalError",
    "Next": "Test Suite Failure"
  },

  "Compose Config": {
    "Type": "Task",
    "Comment": "Trigger the configuration composition",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${ConfigComposerLambdaName}",
      "Payload": { "environment": "${DeploymentEnvironment}" }
    },
    "ResultPath": "$.ConfigComposeResult",
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
        "Next": "Enrich Compose Config Error"
      }
    ],
    "Next": "Skip Env Setup Decision"
  },

  "Enrich Compose Config Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Configuration Composer Lambda failed.",
      "SourceState": "Compose Config",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Skip Env Setup Decision": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.SkipEnvSetup",
        "BooleanEquals": true,
        "Next": "Collect Commit Hashes"
      }
    ],
    "Default": "Trigger Environment Setup"
  }
}
