# Infrastructure

This directory contains Terraform configuration for E2E AWS infrastructure, including Lambda layers for shared Python modules.

## Prerequisites

- Terraform >= 1.13
- AWS CLI configured with appropriate credentials
- Python 3.13 (or compatible version)
- pip

## Architecture

This infrastructure deploys:
1. **Lambda Layer** - Shared Python dependencies (pydantic, httpx)
2. **Approval Handler Lambda** - Processes SNS approval messages
3. **IAM Roles** - Proper permissions for Lambda execution
4. **CloudWatch Log Groups** - Centralized logging
5. **Test Execution Orchestrator** - Step function orchestrating the E2E flow
6. **DynamoDB E2E execution table** - DB records used to keep state of E2E workflows

## Lambda Layer

The Lambda layer includes:
- Shared Python modules from `src/shared/`
- Python dependencies (pydantic, httpx) specified in `src/shared/requirements.txt`

### Usage

#### 1. Initial Setup - Build Artifacts

Lambda changes (by artifact hash comparison) should be automatically recognized by Terraform resources and rebuild if needed.

If they are not - Before running `terraform plan` or `terraform apply` for the first time, build the Lambda artifacts:

```bash
cd infra/terraform/modules/lambda_layer

# Build artifacts gradually
./build_layer.sh
./build_lambda.sh approval_handler
./build_lambda.sh commit_collector
./build_lambda.sh execution_record_handler
./build_lambda.sh reporter
./build_lambda.sh config_composer
./build_lambda.sh deployment_checker
./build_lambda.sh setup_trigger
./build_lambda.sh execution_params_validator
./build_lambda.sh dp_password_rotator
./build_lambda.sh deployment_data_extractor

# ... or build all of them at once
./build_all_artifacts.sh

```

This creates:
- `layer_build/lambda_layer.zip` - Shared modules and dependencies
- `layer_build/approval_handler.zip` - Lambda
- `layer_build/commit_collector.zip` - Lambda
- `layer_build/execution_record_handler.zip` - Lambda
- `layer_build/reporter.zip` - Lambda
- `layer_build/config_composer.zip` - Lambda
- `layer_build/deployment_checker.zip` - Lambda
- `layer_build/setup_trigger.zip` - Lambda
- `layer_build/execution_params_validator.zip` - Lambda
- `layer_build/dp_password_rotator.zip` - Lambda
- `layer_build/deployment_data_extractor.zip` - Lambda

After the initial build, Terraform will automatically rebuild when code changes.

#### 2. Deploy with Terraform

Now you can deploy the infrastructure:

```bash
# Initialize Terraform (first time only)
terraform init

# Review what will be created
terraform plan

# Deploy the resources
terraform apply
```

### Outputs

After deployment, Terraform provides these outputs:

```bash
terraform output lambda_layer_arn              # Layer ARN (without version)
terraform output lambda_layer_version_arn      # Layer ARN with version
terraform output lambda_layer_version          # Version number
terraform output lambda_layer_name             # Layer name
```

### Automatic Rebuilds

The layer is automatically rebuilt when:
- Files in `src/shared/` change
- `src/shared/requirements.txt` changes
- `build_layer.sh` script changes

Terraform tracks these changes using file hashes and triggers rebuilds as needed.

### Layer Contents

The layer follows AWS Lambda's directory structure:

```
python/
├── shared/              # Your shared modules
│   ├── __init__.py
│   └── requirements.txt
├── pydantic/            # Installed dependency
├── httpx/               # Installed dependency
└── ...                  # Other dependencies
```

Import shared modules like this:

```python
from shared import my_module  # Custom modules
import pydantic               # Layer dependencies
import httpx                  # Layer dependencies
```

## Approval Handler Lambda

The approval handler Lambda function automatically processes SNS approval messages.

### Function Details

- **Runtime**: Python 3.13
- **Handler**: `approval_handler.handler.lambda_handler`
- **Timeout**: 60 seconds (configurable)
- **Memory**: 256 MB (configurable)
- **Layer**: Uses the shared layer for dependencies

### Invoking the Function

**Manual test invocation:**

```bash
aws lambda invoke \
  --function-name $(terraform output -raw approval_handler_function_name) \
  --payload file://test_event.json \
  response.json
```

**Example test event (test_event.json):**

```json
{
  "Records": [
    {
      "Sns": {
        "TopicArn": "arn:aws:sns:us-east-1:123456789:test-topic",
        "MessageId": "test-123",
        "Message": "Your SNS message content here..."
      }
    }
  ]
}
```

### SNS Integration

To connect the Lambda to an SNS topic, uncomment the SNS subscription section in `lambda_approval_handler.tf`:

```hcl
resource "aws_sns_topic_subscription" "approval_handler" {
  topic_arn = aws_sns_topic.approval_notifications.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.approval_handler.arn
}

resource "aws_lambda_permission" "allow_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.approval_handler.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.approval_notifications.arn
}
```

### Troubleshooting

**Build fails with "command not found: sha256sum"**
- On macOS, install coreutils: `brew install coreutils`
- Or modify `build_layer.sh` to use `shasum -a 256` instead

**Layer size too large**
- Lambda layers have a 50MB compressed / 250MB uncompressed limit
- Remove unnecessary dependencies
- Use `--no-deps` for specific packages in requirements.txt

**Import errors in Lambda**
- Ensure the layer is attached to your function
- Check Python runtime compatibility
- Verify the import path (should be `from shared import ...`)

## Test Execution Orchestrator Module

This project includes a reusable Test Execution Orchestrator module for orchestrating E2E test suite execution. The module is implemented in `modules/test_execution_orchestrator` and leverages AWS Test Execution Orchestrator to coordinate validation, environment setup, test execution, and reporting steps for E2E workflows. The state machine definition is managed as a JSON template and rendered via Terraform.

### Required Execution Parameters

To start an execution of the E2E SFN, you must provide the following input parameters:

- `OsduVersion` (string) {required}: OSDU version to test (e.g., `r3m23`, `r3m24`, `r3m25`).
- `EnterpriseProductTypeActive` (boolean) {required}: Whether the Enterprise product type is active.
- `SkipEnvSetup` (boolean) {optional}: Whether to skip Environment Setup step during execution.
- `DataPortalAccountId` (string): Data Portal target AWS account ID.
- `DeploymentRoleName` (string): Data Portal IAM Role name with all permissions required by deployment.
- `DataPortalDomain` (string): Data Portal deployment URL (bare domain format) (attached inside Route53 config).
- `DataPortalHostedZoneId` (string): Route53 Hosted Zone ID (`Z<id>` format).
- `DryRun` (boolean): Runs SFN suite to Operation Portal tests but does not trigger Data Portal deployment.
- `TeardownTriggerActive` (boolean): Flag that whether to trigger teardown or not.

These parameters are validated at the start of the workflow. See the `test_suite_execution_param_validation.json.tpl` for details on validation logic.

Detailed E2E test orchestrator can be found within `test_suite_execution.json.tpl` file.

Example payload:
```json
{
  "OsduVersion":  "r3m25",
  "EnterpriseProductTypeActive":  true,
  "DataPortalAccountId":  "018955241485",
  "DeploymentRoleName":  "edi-e2e-tests-custom-fulfillment-role",
  "DataPortalDomain":  "e2e-test-suite.edi.internal0.dataops.47lining.com",
  "DataPortalHostedZoneId":  "Z03189402G93GYQF24E39",
  "DryRun": false,
  "SkipEnvSetup": false,
  "TeardownTriggerActive": true
}
```

### Cost Considerations

- Lambda layers are stored in S3 (free tier: 5GB)
- Each layer version is stored separately
- Old versions can be deleted manually if needed

### Security

- The build script installs dependencies with `--only-binary=:all:` for security
- Compiled dependencies are platform-specific (manylinux2014_x86_64)
- Review `requirements.txt` regularly for security updates

## Module: config composer

The `config_composer` module provisions a small helper Lambda and several SSM parameters and Secrets used by the E2E environment to bootstrap an operations portal and test accounts.

What it creates
- Lambda: a `config_composer` Lambda function that reads SSM parameters and Secrets and returns a composed configuration payload.
- SSM Parameters:
  - `/.../test_admin_user_name` : admin username used by the E2E test account (value used for login)
  - `/.../operations_portal_url` : URL for the operations portal for the target environment
  - `/.../test_inbox_address` : mailbox URL used for inbox verification in tests
- Secrets (Secrets Manager):
  - `/.../test_admin_user_password` : secret containing the admin user's password
  - `/.../test_inbox_password` : secret used for mailbox/inbox password if applicable

Lambda output
The `config_composer` Lambda returns a JSON payload that wraps the `ConfigComposerResult` model. The top-level fields emitted by the Lambda are:

- `admin_username` : string — the admin username (from SSM)
- `admin_username_arn` : string — ARN of the SSM parameter containing the admin username
- `operations_portal_url` : string — the operations portal URL (from SSM)
- `operations_portal_url_arn` : string — ARN of the SSM parameter for the operations portal URL
- `admin_password_arn` : string — ARN of the Secrets Manager secret containing the admin password
- `bb_env_code`: string — the environment code (e.g., short identifier for the environment, from SSM)
- `bb_env_code_arn`: string — ARN of the SSM parameter containing the environment code
- `bb_env_name`: string — the full environment name (e.g., descriptive name for the environment, from SSM)
- `bb_env_name_arn`: string — ARN of the SSM parameter containing the environment name

These values are available as Terraform outputs at the root level after `terraform apply` (prefixed with `config_composer_...`). For example:

```bash
terraform output config_composer_admin_password_secret_arn
terraform output config_composer_admin_username_parameter_name
terraform output config_composer_lambda_function_arn
```

## Manual steps

Post-deploy steps (one-time tasks when deploying E2E stack to a new environment)

After `terraform apply`, a few manual operations are required to prepare the environment for E2E runs. The following checklist describes the minimal manual flow:

1. Secrets initialization
  - Terraform creates `Secrets Manager` secret resources and initial secret versions using a placeholder string `sensitive_value_changed_in_aws_console`. This is intentional so Terraform does not store real credentials in code. After deployment you MUST manually update the secret value in the Secrets Manager console (or via the AWS CLI) with the real password(s) you want the environment to use. A common pattern is to copy the secret values from an existing, trusted environment and paste them into the newly created secret's value.

2. Verify SES sending identity
  - Add the SES identity (email address or domain) you intend to use for notifications and test inboxes in the AWS SES console for the deployed account/region.
  - Follow SES's verification process (you will receive a verification email or need to add DNS records for domain verification).

3. Verify the inbox (test mailbox)
  - If you are using a mailbox (WorkMail or other) for the `test_inbox_address`, make sure the mailbox is reachable and you can view incoming verification emails.
  - If the inbox requires a password that the stack created as a secret, locate the secret ARN via Terraform output and retrieve the secret in the console (or via CLI) to see the password.

4. Login to the operations portal as the admin user
  - Obtain the admin username from SSM (Terraform output for `admin_username_parameter_name`) and the admin password from Secrets Manager (`admin_password_secret_arn`).
  - Use the admin credentials to sign into the Operations Portal UI for the deployed environment.

5. Subscribe and confirm your new E2E email account to `rps_approval_email_sns_topic` backplane SNS topic.

6. (Optional) Re-login as the new user and confirm password flow
  - If the test setup expects a particular password value stored in Secrets Manager, either set that password when creating the user or change the user's password to the value stored in the secret.
  - Re-login to ensure the new account works with the password stored in Secrets Manager.

Notes
- Where the README examples show parameter names, replace `...` with your environment-specific prefix (the Terraform `resource_prefix` and `service_name` determine the final SSM/Secrets names — see `modules/config_composer/locals.tf`).
- For automation, you can script these manual steps using the AWS CLI and portal APIs where available (the README describes the manual flow for clarity and one-off deployments).
