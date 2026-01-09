{
  "Operations Portal Tests": {
    "Type": "Task",
    "Comment": "Trigger portal tests execution within AWS Code Build",
    "Resource": "arn:aws:states:::codebuild:startBuild.sync",
    "Parameters": {
      "ProjectName": "${E2eTestsProjectArn}",
      "BuildspecOverride": "buildspecs/buildspec-operations-portal.yml",
      "EnvironmentVariablesOverride": [
        { "Name": "EXECUTION_ID", "Value.$": "$.DbInitResult.Payload.body.db_record.Id", "Type": "PLAINTEXT" },
        { "Name": "OP_URL", "Value.$": "$.ConfigComposeResult.Payload.body.operations_portal_url", "Type": "PLAINTEXT" },
        { "Name": "E2E_USER", "Value.$": "$.ConfigComposeResult.Payload.body.admin_username", "Type": "PLAINTEXT" },
        { "Name": "OP_PASSWORD", "Value.$": "$.ConfigComposeResult.Payload.body.admin_password_arn", "Type": "SECRETS_MANAGER" },
        { "Name": "DP_DEPLOYMENT_ROLE_NAME", "Value.$": "$.DeploymentRoleName", "Type": "PLAINTEXT" },
        { "Name": "DP_ACCOUNT_ID", "Value.$": "$.DataPortalAccountId", "Type": "PLAINTEXT" },
        { "Name": "DP_DOMAIN", "Value.$": "$.DataPortalDomain", "Type": "PLAINTEXT" },
        { "Name": "DP_HOSTED_ZONE_ID", "Value.$": "$.DataPortalHostedZoneId", "Type": "PLAINTEXT" },
        { "Name": "OSDU_VERSION", "Value.$": "$.OsduVersion", "Type": "PLAINTEXT" },
        { "Name": "ENTERPRISE_ACTIVE", "Value.$": "States.Format('{}', $.EnterpriseProductTypeActive)", "Type": "PLAINTEXT" },
        { "Name": "DRY_RUN_ACTIVE", "Value.$": "States.Format('{}', $.DryRun)", "Type": "PLAINTEXT" },
        { "Name": "REGION", "Value": "${Region}", "Type": "PLAINTEXT" }
      ]
    },
    "ResultPath": "$.OperationsPortalTestsResult",
    "TimeoutSeconds": 1800,
    "Catch": [
      {
        "ErrorEquals": [ "States.TaskFailed" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich OpPortal Test Failure"
      },
      {
        "ErrorEquals": [ "States.Timeout" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich OpPortal Timeout"
      },
      {
        "ErrorEquals": [ "States.ALL" ],
        "ResultPath": "$.RawError",
        "Next": "Enrich OpPortal System Error"
      }
    ],
    "Next": "Deployment Data Extractor"
  },

  "Enrich OpPortal Test Failure": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Operations Portal CodeBuild executed but tests failed.",
      "SourceState": "Operations Portal Tests",
      "TechnicalError": "CodeBuildTestFailure",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich OpPortal Timeout": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Operations Portal tests timed out (exceeded 30 mins).",
      "SourceState": "Operations Portal Tests",
      "TechnicalError": "Timeout",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Enrich OpPortal System Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "System error trying to start Operations Portal CodeBuild.",
      "SourceState": "Operations Portal Tests",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Deployment Data Extractor": {
    "Comment": "Extract deployment data using Deployment Data Extractor Lambda",
    "Type": "Task",
    "Resource": "arn:aws:states:::lambda:invoke",
    "Parameters": {
      "FunctionName": "${DeploymentDataExtractorLambdaName}",
      "Payload": {
        "execution_id.$": "$.DbInitResult.Payload.body.db_record.Id"
      }
    },
    "ResultPath": "$.DeploymentDataExtractorResult",
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
        "Next": "Enrich Deployment Data Extractor Error"
      }
    ],
    "Next": "Dry Run Decision"
  },
  "Enrich Deployment Data Extractor Error": {
    "Type": "Pass",
    "Parameters": {
      "SemanticMessage": "Failed to extract deployment data after Operations Portal tests.",
      "SourceState": "Deployment Data Extractor",
      "TechnicalError.$": "$.RawError.Error",
      "DbRecordId.$": "$.DbInitResult.Payload.body.db_record.Id"
    },
    "ResultPath": "$.GlobalError",
    "Next": "Generate Failure Report"
  },

  "Dry Run Decision": {
    "Type": "Choice",
    "Choices": [
      {
        "Variable": "$.DryRun",
        "BooleanEquals": true,
        "Next": "Generate Success Report"
      }
    ],
    "Default": "Data Portal Website Pooler Init"
  }
}
