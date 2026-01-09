{
  "Teardown Tests": {
    "Type": "Task",
    "Comment": "Trigger teardown tests execution within AWS Code Build",
    "Resource": "arn:aws:states:::codebuild:startBuild.sync",
    "Parameters": {
      "ProjectName": "${E2eTestsProjectArn}",
      "BuildspecOverride": "buildspecs/buildspec-teardown.yml",
      "EnvironmentVariablesOverride": [
        { "Name": "EXECUTION_ID", "Value.$": "$.DbInitResult.Payload.body.db_record.Id", "Type": "PLAINTEXT" },
        { "Name": "OP_URL", "Value.$": "$.ConfigComposeResult.Payload.body.operations_portal_url", "Type": "PLAINTEXT" },
        { "Name": "E2E_USER", "Value.$": "$.ConfigComposeResult.Payload.body.admin_username", "Type": "PLAINTEXT" },
        { "Name": "OP_PASSWORD", "Value.$": "$.ConfigComposeResult.Payload.body.admin_password_arn", "Type": "SECRETS_MANAGER" },
        { "Name": "DEPLOYMENT_ID", "Value.$": "$.DeploymentDataExtractorResult.Payload.body.deployment_id", "Type": "PLAINTEXT" },
        { "Name": "TEARDOWN_TRIGGER_ACTIVE", "Value.$": "States.Format('{}', $.TeardownTriggerActive)", "Type": "PLAINTEXT" }
      ]
    },
    "ResultPath": "$.TeardownTestsResult",
    "TimeoutSeconds": 1800,
    "Catch": [
      {
        "ErrorEquals": [ "States.TaskFailed" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Teardown Test Failure"
      },
      {
        "ErrorEquals": [ "States.Timeout" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Teardown Timeout"
      },
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Teardown System Error"
      }
    ],
    "Next": "Check Teardown Tests"
  },

  "Enrich Teardown Test Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Teardown CodeBuild executed but tests failed.",
      "SourceState": "Teardown Tests",
      "TechnicalError": "CodeBuildTestFailure",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich Teardown Timeout": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Teardown tests timed out.",
      "SourceState": "Teardown Tests",
      "TechnicalError": "Timeout",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich Teardown System Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "System error trying to start Teardown CodeBuild.",
      "SourceState": "Teardown Tests",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Check Teardown Tests": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.TeardownTestsResult.result",
        "BooleanEquals": true,
        "Next": "Data Portal Website Teardown Pooler"
      }
    ],
    "Default": "Enrich Teardown Logic Failure"
  },

  "Enrich Teardown Logic Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Teardown Tests returned false result (Logic Failure).",
      "SourceState": "Check Teardown Tests",
      "TechnicalError": "TestResultFalse",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Data Portal Website Teardown Pooler": {
    "Type": "Task",
    "Resource": "arn:aws:states:::http:invoke",
    "Parameters": {
      "ApiEndpoint.$": "States.Format('https://{}', $.DataPortalDomain)",
      "Authentication": { "ConnectionArn": "${DataPortalConnectionArn}" },
      "Method": "GET",
      "QueryParameters": { "timeout": 30 }
    },
    "TimeoutSeconds": 30,
    "Retry": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "IntervalSeconds": 900,
        "MaxAttempts": 12,
        "BackoffRate": 1.0
      }
    ],
    "Catch": [
      {
        "ErrorEquals": [ "States.Timeout", "States.TaskFailed" ],
        "Next": "Generate Success Report"
      },
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich Teardown Pooler Error"
      }
    ],
    "Next": "Check DataPortal Website Teardown Pooler"
  },

  "Enrich Teardown Pooler Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Teardown verification (website down check) encountered a system error.",
      "SourceState": "Data Portal Website Teardown Pooler",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Check DataPortal Website Teardown Pooler": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.DataPortalPoolerResult.ResponseBody",
        "IsNull": true,
        "Next": "Generate Success Report"
      }
    ],
    "Default": "Enrich Teardown Verification Failure"
  },

  "Enrich Teardown Verification Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Teardown verification failed: The Website is still accessible.",
      "SourceState": "Check DataPortal Website Teardown Pooler",
      "TechnicalError": "WebsiteStillUp",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  }
}
