{
  "Data Portal Website Pooler Init": {
    "Type": "Pass",
    "Result": 0,
    "ResultPath": "$.DataPortalRetryCount",
    "Next": "Data Portal Website Pooler"
  },

  "Data Portal Website Pooler": {
    "Type": "Task",
    "Comment": "Check the data portal website availability with retry",
    "Resource": "arn:aws:states:::http:invoke",
    "Parameters": {
      "ApiEndpoint.$": "States.Format('https://{}', $.DataPortalDomain)",
      "Authentication": { "ConnectionArn": "${DataPortalConnectionArn}" },
      "Method": "GET",
      "QueryParameters": { "timeout": 30 }
    },
    "TimeoutSeconds": 30,
    "ResultPath": "$.DataPortalPoolerResult",
    "Retry": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "IntervalSeconds": 900,
        "MaxAttempts": 22,
        "BackoffRate": 1.0
      }
    ],
    "Catch": [
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Pooler Error"
      }
    ],
    "Next": "Check DataPortal Website Pooler"
  },

  "Enrich DataPortal Pooler Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Unable to reach Data Portal Website (HTTP Request Failed).",
      "SourceState": "Data Portal Website Pooler",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Check DataPortal Website Pooler": {
    "Type": "Choice",
    "Comment": "Branch based on data portal website availability",
    "Choices": [
      {
        "Variable": "$.DataPortalPoolerResult.ResponseBody",
        "StringMatches": "*Open Subsurface Data Universe Platform Console*",
        "Next": "Password Rotator"
      }
    ],
    "Default": "Enrich DataPortal Content Mismatch"
  },

  "Enrich DataPortal Content Mismatch": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Data Portal Website is reachable but content validation failed (String mismatch).",
      "SourceState": "Check DataPortal Website Pooler",
      "TechnicalError": "ContentVerificationFailed",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Password Rotator": {
    "Type": "Task",
    "Comment": "Trigger the password rotator lambda",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${PasswordRotatorLambdaName}",
      "Payload": {
        "environment": "${DeploymentEnvironment}",
        "e2e_user.$": "$.ConfigComposeResult.Payload.body.admin_username",
        "dp_account_id.$": "$.DataPortalAccountId"
      }
    },
    "ResultPath": "$.PasswordRotatorResult",
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
        "Next": "Enrich Password Rotator Error"
      }
    ],
    "Next": "Data Portal Activation Tests"
  },

  "Enrich Password Rotator Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Password Rotator Lambda failed.",
      "SourceState": "Password Rotator",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Data Portal Activation Tests": {
    "Type": "Task",
    "Comment": "Run data portal activation tests to turn on the platform",
    "Resource": "arn:aws:states:::codebuild:startBuild.sync",
    "Parameters": {
      "ProjectName": "${E2eTestsProjectArn}",
      "BuildspecOverride": "buildspecs/buildspec-data-portal-activation.yml",
      "EnvironmentVariablesOverride": [
        { "Name": "EXECUTION_ID", "Value.$": "$.DbInitResult.Payload.body.db_record.Id", "Type": "PLAINTEXT" },
        { "Name": "DP_DOMAIN", "Value.$": "$.DataPortalDomain", "Type": "PLAINTEXT" },
        { "Name": "E2E_USER", "Value.$": "$.ConfigComposeResult.Payload.body.admin_username", "Type": "PLAINTEXT" },
        { "Name": "DP_PASSWORD_ARN", "Value.$": "$.PasswordRotatorResult.Payload.body.dp_password_arn", "Type": "PLAINTEXT" },
        { "Name": "CROSS_ACCOUNT_ROLE_ARN", "Value.$": "$.PasswordRotatorResult.Payload.body.cross_account_role_arn", "Type": "PLAINTEXT" }
      ]
    },
    "ResultPath": "$.DataPortalActivationResult",
    "TimeoutSeconds": 600,
    "Catch": [
      {
        "ErrorEquals": [ "States.TaskFailed" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Activation Failure"
      },
      {
        "ErrorEquals": [ "States.Timeout" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Activation Timeout"
      },
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Activation System Error"
      }
    ],
    "Next": "Wait for Activation Propagation"
  },

  "Wait for Activation Propagation": {
    "Type": "Wait",
    "Comment": "Wait 15 minutes for Data Portal activation to propagate",
    "Seconds": 900,
    "Next": "Data Portal Verification Tests"
  },

  "Data Portal Verification Tests": {
    "Type": "Task",
    "Comment": "Run data portal verification tests",
    "Resource": "arn:aws:states:::codebuild:startBuild.sync",
    "Parameters": {
      "ProjectName": "${E2eTestsProjectArn}",
      "BuildspecOverride": "buildspecs/buildspec-data-portal-verification.yml",
      "EnvironmentVariablesOverride": [
        { "Name": "EXECUTION_ID", "Value.$": "$.DbInitResult.Payload.body.db_record.Id", "Type": "PLAINTEXT" },
        { "Name": "DP_DOMAIN", "Value.$": "$.DataPortalDomain", "Type": "PLAINTEXT" },
        { "Name": "E2E_USER", "Value.$": "$.ConfigComposeResult.Payload.body.admin_username", "Type": "PLAINTEXT" },
        { "Name": "DP_PASSWORD_ARN", "Value.$": "$.PasswordRotatorResult.Payload.body.dp_password_arn", "Type": "PLAINTEXT" },
        { "Name": "CROSS_ACCOUNT_ROLE_ARN", "Value.$": "$.PasswordRotatorResult.Payload.body.cross_account_role_arn", "Type": "PLAINTEXT" }
      ]
    },
    "ResultPath": "$.DataPortalVerificationResult",
    "TimeoutSeconds": 1200,
    "Catch": [
      {
        "ErrorEquals": [ "States.TaskFailed" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Verification Failure"
      },
      {
        "ErrorEquals": [ "States.Timeout" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Verification Timeout"
      },
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich DataPortal Verification System Error"
      }
    ],
    "Next": "Teardown Tests"
  },

  "Enrich DataPortal Activation Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Data Portal Activation CodeBuild executed but tests failed.",
      "SourceState": "Data Portal Activation Tests",
      "TechnicalError": "CodeBuildTestFailure",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich DataPortal Activation Timeout": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Data Portal Activation tests timed out (exceeded 10 mins).",
      "SourceState": "Data Portal Activation Tests",
      "TechnicalError": "Timeout",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich DataPortal Activation System Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "System error trying to start Data Portal Activation CodeBuild.",
      "SourceState": "Data Portal Activation Tests",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich DataPortal Verification Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Data Portal Verification CodeBuild executed but tests failed.",
      "SourceState": "Data Portal Verification Tests",
      "TechnicalError": "CodeBuildTestFailure",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich DataPortal Verification Timeout": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Data Portal Verification tests timed out (exceeded 20 mins).",
      "SourceState": "Data Portal Verification Tests",
      "TechnicalError": "Timeout",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich DataPortal Verification System Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "System error trying to start Data Portal Verification CodeBuild.",
      "SourceState": "Data Portal Verification Tests",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  }
}
