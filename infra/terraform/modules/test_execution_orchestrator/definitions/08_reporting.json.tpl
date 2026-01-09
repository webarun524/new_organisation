{
  "Generate Success Report": {
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Comment": "Generate the success report for the workflow",
    "Parameters": {
      "FunctionName": "${ReporterLambdaName}",
      "Payload": {
        "Id.$": "$.DbInitResult.Payload.body.db_record.Id",
        "IsSuccess": true
      }
    },
    "Retry": [
      {
        "ErrorEquals": [
          "Lambda.ServiceException",
          "Lambda.AWSLambdaException",
          "Lambda.SdkClientException"
        ],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2
      }
    ],
    "Catch": [
      {
        "ErrorEquals": [
          "States.ALL"
        ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Generate Success Report Failure"
      }
    ],
    "ResultPath": "$.GenerateSuccessReportResult",
    "Next": "Check Generate Success Report"
  },
  "Check Generate Success Report": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.GenerateSuccessReportResult.Payload.statusCode",
        "NumericEquals": 200,
        "Next": "Update E2E DB Record - Success"
      }
    ],
    "Default": "Enrich Generate Success Report Failure"
  },
  "Enrich Generate Success Report Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to generate the final success report artifact.",
      "SourceState": "Generate Success Report",
      "TechnicalError": "ReportGenerationFailed",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },
  "Update E2E DB Record - Success": {
    "Type": "Task",
    "Comment": "Update db record to success status",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${ExecutionRecordLambdaName}",
      "Payload": {
        "Status": "success",
        "Id.$": "$.DbInitResult.Payload.body.db_record.Id"
      }
    },
    "ResultPath": "$.DbUpdateSuccessReportResult",
    "Next": "Success"
  },
  "Success": {
    "Type": "Succeed",
    "Comment": "Workflow succeeded"
  },

  "Generate Failure Report": {
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Comment": "Generate the failure report for the workflow",
    "Parameters": {
      "FunctionName": "${ReporterLambdaName}",
      "Payload": {
        "Id.$": "$.DbInitResult.Payload.body.db_record.Id",
        "IsSuccess": false,
        "ErrorDetails.$": "$.GlobalError"
      }
    },
    "Retry": [
      {
        "ErrorEquals": [
          "Lambda.ServiceException",
          "Lambda.AWSLambdaException",
          "Lambda.SdkClientException"
        ],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2
      }
    ],
    "ResultPath": "$.GenerateFailureReportResult",
    "Next": "Update E2E DB Record - Failure"
  },
  "Update E2E DB Record - Failure": {
    "Type": "Task",
    "Comment": "Update db record to failure status",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${ExecutionRecordLambdaName}",
      "Payload": {
        "Status": "failure",
        "Id.$": "$.DbInitResult.Payload.body.db_record.Id",
        "FailureReason.$": "States.JsonToString($.GlobalError)"
      }
    },
    "ResultPath": "$.DbUpdateFailureReportResult",
    "Next": "Test Suite Failure"
  },
  "Test Suite Failure": {
    "Type": "Fail",
    "Comment": "Workflow failed due to an error or unmet condition",
    "CausePath": "$.GlobalError.SemanticMessage",
    "ErrorPath": "$.GlobalError.SourceState"
  }
}
