{
  "Collect Commit Hashes": {
    "Comment": "Call Lambda to collect commit hashes from repositories",
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${CommitCollectorLambdaName}",
      "Payload": {
        "osdu_version.$": "$.OsduVersion",
        "environment": "${DeploymentEnvironment}",
        "bb_env_code.$": "$.ConfigComposeResult.Payload.body.bb_env_code",
        "bb_env_name.$": "$.ConfigComposeResult.Payload.body.bb_env_name"
      }
    },
    "ResultPath": "$.CollectCommitResult",
    "TimeoutSeconds": 1800,
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
        "Next": "Enrich Commit Collection Error"
      }
    ],
    "Next": "Check Commit Result"
  },

  "Enrich Commit Collection Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to collect commit hashes from repositories.",
      "SourceState": "Collect Commit Hashes",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Check Commit Result": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.CollectCommitResult.Payload.body.error",
        "IsPresent": true,
        "Next": "Enrich Commit Logic Failure"
      }
    ],
    "Default": "Update E2E DB Record - Environment Initialized"
  },

  "Enrich Commit Logic Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Commit Collector Lambda returned empty or invalid result.",
      "SourceState": "Check Commit Result",
      "TechnicalError": "MissingCommitHashes",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Update E2E DB Record - Environment Initialized": {
    "Type": "Task",
    "Comment": "Update db record with environmental setup",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${ExecutionRecordLambdaName}",
      "Payload": {
        "Id.$": "$.DbInitResult.Payload.body.db_record.Id",
        "Status": "deployedServices",
        "DeployedServices.$": "$.CollectCommitResult.Payload.body"
      }
    },
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
        "Next": "Enrich DB Update Env Failure"
      }
    ],
    "ResultPath": "$.DbUpdateEnvResult",
    "Next": "Check Update E2E DB Record - Environment Initialized"
  },

  "Check Update E2E DB Record - Environment Initialized": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.DbUpdateEnvResult.Payload.statusCode",
        "NumericEquals": 200,
        "Next": "Operations Portal Tests"
      }
    ],
    "Default": "Enrich DB Update Env Failure"
  },

  "Enrich DB Update Env Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to update Database with Environment Initialization status.",
      "SourceState": "Update E2E DB Record - Environment Initialized",
      "TechnicalError": "DBUpdateFailed",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  }
}
