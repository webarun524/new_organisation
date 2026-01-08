{
  "Validate Input": {
    "Type": "Task",
    "Comment": "Entry point of the E2E orchestration",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${SfnValidatorFunctionName}",
      "Payload": {
        "OsduVersion.$": "$.OsduVersion",
        "EnterpriseProductTypeActive.$": "$.EnterpriseProductTypeActive",
        "DryRun.$": "$.DryRun",
        "SkipEnvSetup.$": "$.SkipEnvSetup",
        "DeploymentRoleName.$": "$.DeploymentRoleName",
        "DataPortalAccountId.$": "$.DataPortalAccountId",
        "DataPortalDomain.$": "$.DataPortalDomain",
        "DataPortalHostedZoneId.$": "$.DataPortalHostedZoneId",
        "TeardownTriggerActive.$": "$.TeardownTriggerActive"
      }
    },
    "ResultPath": "$.ValidationResult",
    "Retry": [
      {
        "ErrorEquals": [ "Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException" ],
        "IntervalSeconds": 2,
        "MaxAttempts": 2,
        "BackoffRate": 2
      }
    ],
    "Catch": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Validation Error"
      }
    ],
    "Next": "Check Validation Result"
  },

  "Enrich Validation Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Input Validator Lambda failed to invoke. Check IAM roles or payload structure.",
      "SourceState": "Validate Input",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId": null
    },
    "ResultPath": "$.GlobalError",
    "Next": "Test Suite Failure"
  },

  "Check Validation Result": {
    "Type": "Choice",
    "Comment": "Check if validation Lambda returned success status",
    "Choices": [
      {
        "Variable": "$.ValidationResult.Payload.statusCode",
        "NumericEquals": 200,
        "Next": "Initialize E2E DB Record"
      }
    ],
    "Default": "Enrich Validation Logic Failure"
  },

  "Enrich Validation Logic Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Input Validation rejected the payload (Non-200 Status).",
      "SourceState": "Check Validation Result",
      "TechnicalError": "ValidationLogicError",
      "Details.$": "$.ValidationResult.Payload.body.message",
      "DbRecordId": null
    },
    "ResultPath": "$.GlobalError",
    "Next": "Test Suite Failure"
  }
}
