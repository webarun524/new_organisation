# Bitbucket OIDC Integration Module

This module establishes OpenID Connect (OIDC) integration between AWS and Bitbucket Pipelines, enabling secure federated authentication without storing AWS credentials in Bitbucket.

## What This Module Does

- Creates an AWS IAM OpenID Connect Provider for Bitbucket
- Sets up an IAM role that Bitbucket Pipelines can assume
- Grants permissions to execute AWS Step Functions (SFN)
- Configures trust relationships with specific Bitbucket subjects

## Prerequisites

1. **AWS Account**: Access to the target AWS account where e2e tests are deployed
2. **Bitbucket Workspace**: Access to the 47Lining Bitbucket workspace
3. **Terraform**: Installed and configured for your AWS account
4. **OpenSSL**: Required to extract the Bitbucket OIDC thumbprint

## Required Terraform Variables

### Required (No Defaults)

- **`sfn_orchestrator_arn`** (string)
  - The ARN of the AWS Step Functions orchestrator that Bitbucket will execute

- **`bitbucket_audience`** (string, sensitive)
  - The Bitbucket workspace identifier in the format: `ari:cloud:bitbucket::workspace/<WORKSPACE_UUID>`
  - To find your workspace UUID:
    1. Log in to Bitbucket
    2. Go to Workspace settings
    3. The UUID is in the workspace details
  - Example: `ari:cloud:bitbucket::workspace/a1b2c3d4-e5f6-7890-abcd-ef1234567890`

- **`bitbucket_oidc_provider_url`** (string)
  - The Bitbucket OIDC provider URL
  - For all Bitbucket Cloud workspaces: `https://api.bitbucket.org/2.0/workspaces/47lining/pipelines-config/identity/oidc`

- **`bitbucket_thumbprint`** (string)
  - The SHA-1 thumbprint of Bitbucket's OIDC provider root certificate (no colons)
  - Reference: [AWS OIDC Thumbprint Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html)

### Optional (With Defaults)

- **`bitbucket_subjects`** (list of strings, default: `["*"]`)
  - List of allowed Bitbucket subjects that can assume the role
  - Subjects control which Bitbucket repositories and pipelines can access this role
  - Examples:
    - `["*"]` - Allow all subjects (less secure, use only for development)
    - `["bitbucket.org:repo_uuid:<repo-uuid>:ref:refs/heads/main"]` - Specific branch
    - `["bitbucket.org:workspace_uuid:47lining:*"]` - All repos in workspace
  - At least one subject must be specified

- **`max_session_duration`** (number, default: `3600`)
  - Maximum session duration in seconds (1 hour default)
  - Valid range: 900 seconds (15 minutes) to 43200 seconds (12 hours)
  - Increase if your Step Function executions need longer than 1 hour
