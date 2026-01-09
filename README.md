# EDI E2E Test Framework - Comprehensive Developer Guide

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Getting Started](#getting-started)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Infrastructure](#infrastructure)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Contributing](#contributing)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The **EDI Automated E2E Test Framework** manages infrastructure and end-to-end tests for the EDI backplane infrastructure and deployment. The project orchestrates comprehensive testing workflows that validate Operations Portal and Data Portal deployments across AWS environments.

### Key Technologies

- **Python 3.13**: Core language for tests and Lambda functions
- **Poetry**: Dependency management and packaging
- **Playwright + pytest**: Browser automation and test framework
- **Terraform**: Infrastructure as Code (IaC)
- **AWS Services**: Lambda, Step Functions, CodeBuild, DynamoDB, S3, Route53
- **Commitizen**: Version management and changelog generation

---

## Repository Structure

```
edi-e2e-tests/
├── src/
│   └── edi_e2e_tests/         # Main package source code
├── e2e/                        # End-to-end test suite
│   ├── tests/
│   │   ├── operations_portal/ # Operations Portal UI tests
│   │   └── data_portal/       # Data Portal UI tests
│   ├── models.py              # Type definitions for test configs
│   └── conftest.py            # Shared pytest fixtures
├── tests/                      # Unit tests
├── infra/                      # Infrastructure as Code
│   ├── terraform/             # Main E2E infrastructure stack
│   │   ├── modules/
│   │   │   ├── lambda_layer/              # Shared Lambda dependencies
│   │   │   ├── bitbucket_permissions/     # OIDC integration
│   │   │   └── test_execution_orchestrator/ # Step Functions orchestration
│   │   │       └── definitions/           # State machine JSON templates (8 phases)
│   │   └── *.tf               # Root Terraform configuration
│   └── data_portal/           # Data Portal helper stack
│       └── terraform/
│           └── modules/
│               └── data_portal_setup/     # Route53 & IAM for custom fulfillment
├── buildscripts/              # Build, deploy, and helper scripts
│   ├── deploy.sh              # Deploy E2E infrastructure
│   ├── destroy.sh             # Destroy E2E infrastructure
│   ├── install-poetry.sh      # Install Poetry
│   ├── install-terraform.sh   # Install Terraform
│   ├── quality.sh             # Run quality checks
│   ├── add_policy_for_approval_lambda.sh   # SNS permissions
│   └── add_ns_record_to_shared_data_portal_layer.sh  # Route53 NS setup
├── buildspecs/                # AWS CodeBuild specifications
│   ├── buildspec.yml                        # Main buildspec
│   ├── buildspec-operations-portal.yml      # Operations Portal tests
│   ├── buildspec-data-portal-activation.yml # Data Portal activation
│   ├── buildspec-data-portal-verification.yml # Data Portal verification
│   └── buildspec-teardown.yml               # Teardown tests
├── bitbucket-pipelines.yml    # Bitbucket CI/CD configuration
├── pyproject.toml             # Poetry project configuration
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── .cz.toml                   # Commitizen configuration
├── Makefile                   # Common development commands
└── README.md                  # Quick start guide
```

### Directory Descriptions

#### `/src/edi_e2e_tests/`
Main Python package containing shared modules and Lambda function code used across the test infrastructure.

#### `/e2e/`
Playwright + pytest based end-to-end tests for Operations Portal and Data Portal. Tests are organized by portal type and must be marked with appropriate pytest markers.

#### `/tests/`
Unit tests for the main package source code.

#### `/infra/terraform/`
Main Terraform stack that provisions:
- Lambda functions and shared Lambda layer
- CodeBuild projects for test execution
- Step Functions state machine for orchestration
- DynamoDB tables for execution tracking
- S3 buckets for artifacts and reports
- IAM roles and policies
- CloudWatch Log Groups

#### `/infra/data_portal/terraform/`
Auxiliary Terraform stack for Data Portal-specific resources:
- Route53 hosted zone for test domains
- IAM role and policy for custom fulfillment operations

#### `/buildscripts/`
Helper scripts for building, deploying, and managing infrastructure.

#### `/buildspecs/`
AWS CodeBuild specifications for different test phases:
- `buildspec.yml` - Main buildspec for general E2E tests
- `buildspec-operations-portal.yml` - Operations Portal test execution
- `buildspec-data-portal-activation.yml` - Data Portal activation tests
- `buildspec-data-portal-verification.yml` - Data Portal verification tests
- `buildspec-teardown.yml` - Teardown test execution

---

## Getting Started

### Prerequisites

- **Python 3.13** (managed via `.python-version`)
- **Poetry** (for dependency management)
- **Terraform >= 1.13** (for infrastructure)
- **AWS CLI** (configured with appropriate credentials)
- **Git** (for version control)

### Initial Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd edi-e2e-tests
```

#### 2. Install Poetry

If Poetry is not installed:

```bash
./buildscripts/install-poetry.sh
# or
curl -sSL https://install.python-poetry.org | python3 -
```

#### 3. Install Dependencies

```bash
# Install project dependencies (including dev dependencies)
poetry install --with dev

# Activate the virtual environment
poetry env source

# Install Playwright browsers
playwright install
```

#### 4. Set Up Pre-commit Hooks

Pre-commit hooks enforce code quality standards:

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually to verify setup
pre-commit run --all-files
```

#### 5. Configure Environment Variables

For local test runs, create a `.env.test` file:

```bash
# Copy the example file
cp e2e/example.env.test e2e/.env.test

# Edit .env.test with your environment-specific values
```

**Required Environment Variables:**

- `E2E_USER` - User email
   - `operations_portal` mark
   - `data_portal_activation` mark
   - `data_portal_verification` mark
   - `data_portal_teardown` mark
- `OSDU_VERSION` - OSDU version (e.g., r3m25)
   - `operations_portal` mark
- `ENTERPRISE_ACTIVE` - Express or Enterprise product type
   - `operations_portal` mark
   - `data_portal_verification` mark
- `DRY_RUN_ACTIVE` - Run tests without triggering deployment
   - `operations_portal` mark
- `REGION` - AWS Region
   - `operations_portal` mark
- `OP_URL` - Operations Portal URL
   - `operations_portal` mark
   - `data_portal_teardown` mark
- `OP_PASSWORD` - Operations Portal password
   - `operations_portal` mark
   - `data_portal_teardown` mark
- `DEPLOYMENT_ID` - ID of Data Portal deployment
   - `data_portal_teardown` mark
- `TEARDOWN_TRIGGER_ACTIVE` - Flag to initiate teardown tests
   - `data_portal_teardown` mark
- `DP_DEPLOYMENT_ROLE_NAME` - Data Portal deployment role name
   - `operations_portal` mark
- `DP_ACCOUNT_ID` - Data Portal AWS account ID
   - `operations_portal` mark
- `DP_DOMAIN` - Data Portal domain
   - `operations_portal` mark
   - `data_portal_activation` mark
   - `data_portal_verification` mark
   - `data_portal_teardown` mark
- `DP_HOSTED_ZONE_ID` - Route53 hosted zone ID
   - `operations_portal` mark
- `DP_PASSWORD` - Data Portal password
   - `data_portal_activation` mark
   - `data_portal_verification` mark

---

## Development Workflow

### Code Quality

The project enforces strict code quality standards:

#### Linting and Formatting

```bash
# Auto-fix linting issues with Ruff
ruff check --fix .

# Format code
ruff format .

# Run both via pre-commit
pre-commit run --all-files
```

#### Configuration

- **Ruff**: Line length 88, Python 3.10+ syntax
- **Rules**: E (Error), F (Pyflakes), W (Warning), I (isort)
- **Exception**: E501 (line-too-long) ignored, formatter handles this

### Version Management

The project uses **Commitizen** for semantic versioning:

```bash
# Add changes to staged changes
git add .

# Create a commit interactively (recommended)
cz commit

# Bump version based on commits
cz bump || cz commit (type `bump`)
```

**Important**: Do NOT push tags unintentionally. Avoid:
- `git push --tags`
- `git push --follow-tags`
- GUI tools may auto-push tags (e.g., GitHub Desktop)

### Commit Convention

Follow the custom Commitizen commit pattern:

```
<type>: <message>
```

**Types:**
- `feat`: New features (bumps MINOR version)
- `fix`: Bug fixes (bumps PATCH version)
- `chore`: Maintenance tasks (bumps PATCH version)
- `bump`: Version bump commits
- `revert`: Reverts previous commits (bumps PATCH version)

**Example:**
```bash
feat: add dark mode toggle to settings
fix: resolve authentication timeout issue
chore: update dependencies to latest versions
```

### Makefile Commands

Use the Makefile for common tasks:

```bash
make help                      # Display all available commands
make install                   # Install Python dependencies
make test                      # Run unit tests
make quality_test              # Run quality checks
make e2e_op_tests              # Run Operations Portal E2E tests
make e2e_dp_verification_tests # Run Data Portal verification tests
make e2e_dp_teardown_tests     # Run Data Portal teardown tests
make build                     # Build application
make deploy                    # Deploy application
make destroy                   # Destroy application
```

---

## Testing

### Test Organization

#### Test Markers

Every E2E test MUST be marked with one of these pytest markers:

- `@pytest.mark.operations_portal`
- `@pytest.mark.data_portal_verification`
- `@pytest.mark.data_portal_teardown`
- `@pytest.mark.data_portal_activation`

**Validation**: Tests without proper markers will fail the run.

#### Test Structure

```
e2e/
├── tests/
│   ├── operations_portal/
│   │   ├── auth/
│   │   │   └── test_login.py
│   │   └── conftest.py       # Portal-specific fixtures
│   ├── data_portal/
│   │   └── ...
│   └── conftest.py           # Shared fixtures
├── models.py                 # Type definitions
└── logs/                     # Test logs
```

### Running Tests

#### Unit Tests

```bash
# Run all unit tests
pytest tests -v

# Or via Make
make test
```

#### E2E Tests Locally

```bash
# Run all E2E tests (requires -m marker)
poetry run pytest e2e -v -m operations_portal

# Run specific test
poetry run pytest e2e/tests/operations_portal/auth/test_login.py::test_sign_in_success -v -m operations_portal

# Headed mode (visible browser)
poetry run pytest e2e -v -m operations_portal --headed --browser chromium

# Slow-motion mode (debugging)
poetry run pytest e2e -v -m operations_portal --slow_mo=200 --browser chromium

# Combine headed + slow-motion
poetry run pytest e2e/tests/operations_portal/auth/test_login.py::test_sign_in_success -v -m operations_portal --headed --slow_mo=1000 --browser chromium
```

#### Running Specific Portal Tests

```bash
# Operations Portal tests
make e2e_op_tests
# or
poetry run pytest e2e -m operations_portal -v

# Data Portal verification tests
make e2e_dp_verification_tests
# or
poetry run pytest e2e -m data_portal_verification -v

# Data Portal teardown tests
make e2e_dp_teardown_tests
# or
poetry run pytest e2e -m data_portal_teardown -v
```

### Test Fixtures

- **Shared fixtures**: `e2e/tests/conftest.py` (browser, env config, marker validation)
- **Portal-specific fixtures**: Each portal folder has its own `conftest.py`
- **Type definitions**: `e2e/models.py` (DpTestConfig, OpTestConfig, etc.)

### Logging

- Tests use a shared logger: `e2e/tests/logger.py`
- Logs written to: `e2e/logs/e2e-tests.log`
- Console output is colored for readability

### Best Practices

- Never commit secrets to the repository
- Use `.env.test` locally (excluded from source control)
- Ensure all tests have proper markers
- Use headed/slow-motion mode for debugging
- Check fixture error messages for missing environment variables

---

## Infrastructure

The project contains **two Terraform stacks** that must be deployed in order.

### Stack 1: Main E2E Infrastructure stack (`infra/terraform`)

Provides e2e infrastructure.

#### What It Provisions

- **Lambda Layer**: Shared Python dependencies (pydantic, httpx)
- **Lambda Functions**:
  - Approval Handler
  - Commit Collector
  - Execution Record Handler
  - Reporter
  - Config Composer
  - Deployment Checker
  - Setup Trigger
  - Execution Params Validator
  - DP Password Rotator
  - Deployment Data Extractor
- **IAM Roles and Policies**: Lambda execution permissions
- **CloudWatch Log Groups**: Centralized logging
- **Step Functions State Machine**: E2E test orchestration (8-phase workflow)
- **DynamoDB Table**: E2E execution state tracking
- **S3 Buckets**: Test reports and artifacts
- **CodeBuild Projects**: Test execution environments
- **SSM Parameters**: Configuration values
- **Secrets Manager**: Sensitive credentials

#### Building Artifacts

Lambda artifacts are automatically rebuilt when code changes. For manual builds:

```bash
cd infra/terraform/modules/lambda_layer

# Build all artifacts at once
./build_all_artifacts.sh

# Or build individually
./build_layer.sh
./build_lambda.sh approval_handler
./build_lambda.sh commit_collector
# ... etc.
```

#### Terraform Vars

- `deployment_environment_code` - type of backplane environment *proto|proto2|proto3|dev|qa|preprod|utility|edi-qa|customer-prod* format
- `backplane_account_id` - Operations Portal AWS account

- `bitbucket_token` - token with access to *dataops-deployments* repository pipelines (https://bitbucket.org/47lining/dataops-deployment/src/main/)

- `bitbucket_audience` - Bitbucket auth integration for E2E repository trigger (https://bitbucket.org/47lining/edi-e2e-tests/src/main/) - *"ari:cloud:bitbucket::workspace/<uuid>"* format
- `bitbucket_thumbprint` - Bitbucket auth integration for E2E repository trigger (https://bitbucket.org/47lining/edi-e2e-tests/src/main/)*"22D2AFA3B2AF7292F120ADBFAD56E654A73FB021"* format
- `bitbucket_subjects` - Bitbucket auth integration for E2E repository trigger (https://bitbucket.org/47lining/edi-e2e-tests/src/main/)- *["{<uuid>}:*"]* format

[Example - *infra/terraform/terraform.tfvars.example*]

#### Deployment

```bash
cd infra/terraform

# Initialize Terraform (first time only)
terraform init

# Review changes
terraform plan

# Deploy infrastructure
terraform apply
```

#### Outputs

```bash
# View Lambda layer information
terraform output lambda_layer_arn
terraform output lambda_layer_version_arn

# View Config Composer outputs
terraform output config_composer_admin_password_secret_arn
terraform output config_composer_lambda_function_arn

# View all outputs
terraform output
```


### Stack 2: Data Portal Stack (`infra/data_portal/terraform`)

Provides infrastructure essential for execution of e2e tests on deployment account.

This Terraform stack should be deployed to AWS account where Data Portal is being deployed. SFN E2E execution parameters are referencing this environment.

#### What It Provisions

- **Route53 Hosted Zone**: Public DNS for test Data Portal domain
- **IAM Role and Policy**: Custom fulfillment operations

#### Deployment

```bash
cd infra/data_portal/terraform

# Initialize
terraform init

# Plan and apply
terraform plan -out plan.tfplan
terraform apply plan.tfplan
```

#### Terraform Vars

- `trusted_accounts` = [
  "013629988812",
  "783764579098",
  "396608783583",
  "997392112313",
  "724930610077",
  "787089968855",
  "412594592849",
  "585008055989",
  "391767403170"
]
- `organization_id` - 47L admin organization ID
- `domain_name` - Data Portal domain name - *domain.com* format

[Example - *infra/data_portal/terraform/terraform.tfvars.example*]


#### Outputs

```bash
# View outputs
terraform output data_portal_custom_fulfillment_role_arn
terraform output data_portal_route53_hosted_zone_id
terraform output data_portal_route53_ns_records
```

### Deployment Order (New Environment)

When deploying to a **new environment**, follow this order:

1. **Add SNS Permissions** (first pass)

   Requires credentials to backplane for deployment confirming lambda to subscribe to approval topic.

   ```bash
   # login to Operations Portal stack AWS account
   export AWS_REGION="us-east-1"
   export SNS_ARN="arn:aws:sns:us-east-1:123456789012:my-approval-topic"
   export E2E_AWS_HOST="123456789012"
   ./buildscripts/add_policy_for_approval_lambda.sh
   ```
   [Target - AWS account where Operations Portal used by E2E tests resides]

2. **Deploy Main Stack**

   ```bash
   # login to Main E2E Stack AWS account
   cd infra/terraform
   terraform init
   terraform plan
   terraform apply
   ```
   [Target - AWS account where E2E resources are ran]

3. **Deploy Data Portal Stack**

   ```bash
   # login to Data Portal stack AWS account
   cd infra/data_portal/terraform
   terraform init
   terraform plan
   terraform apply
   ```
   [Target - AWS account where Operations Portal is deploying Data Portal]

4. **Add Route53 record to shared services**

   ```bash
   # login to shared services `126748958625` stack AWS account
   export DOMAIN_NAME="e2e-test-suite.edi.internal0.dataops.47lining.com"
   export RECORD_NS_VALUE=$'ns-592.awsdns-10.net.\nns-1327.awsdns-37.org.\nns-1856.awsdns-40.co.uk.\nns-490.awsdns-61.com.'
   ./buildscripts/add_policy_for_approval_lambda.sh
   ```
   [Target - shared services AWS account *126748958625*]


### Post-Deployment Manual Steps

After `terraform apply`, complete these manual tasks:

#### 1. Initialize Secrets

Terraform creates placeholder secrets with value `sensitive_value_changed_in_aws_console`.

**Action**: Update secrets in AWS Secrets Manager console with real credentials:
- `/edi/e2e/tests/test_admin_user_password`
- `/edi/e2e/tests/test_inbox_password`

[Target - Main E2E stack]

#### 2. Verify SES Sending Identity

**Action**: Add and verify your email/domain in AWS SES console:
1. Go to SES console for deployed region
2. Add identity (email or domain)
3. Complete verification process

[Target - Operations Portal stack]

#### 3. Verify Test Inbox

**Action**: Ensure the test mailbox is accessible:
1. Check `/edi/e2e/tests/test_inbox_address` from SSM parameter
2. Verify you can receive emails
3. Retrieve mailbox password from Secrets Manager if needed

[Target - Main E2E stack]

#### 4. Login to Operations Portal

**Action**: Test admin user access:
1. Get admin username from SSM: `/edi/e2e/tests/test_admin_user_name`
2. Get password from Secrets Manager: `/edi/e2e/tests/test_admin_user_password`
3. Login to Operations Portal to confirm access

[Target - Operations Portal referenced in Main E2E stack - `infra/terraform/modules/config_composer/locals.tf`]

#### 5. Subscribe to SNS Approval Topic

**Action**: Subscribe E2E email account to `rps_approval_email_sns_topic`:
1. Subscribe to the SNS topic in the backplane account
2. Confirm subscription via email

[Target - Operations Portal stack]

### Step Functions State Machine

The E2E orchestration workflow is split into **8 logical phases**:

```
01_validation.json.tpl           → Input parameter validation
02_initialization.json.tpl       → Database and config initialization
03_environment_setup.json.tpl    → Environment deployment with polling
04_commit_collection.json.tpl    → Repository commit hash collection
05_operations_portal.json.tpl    → Operations Portal test execution
06_data_portal.json.tpl          → Data Portal deployment/verification
07_teardown.json.tpl             → Teardown execution and verification
08_reporting.json.tpl            → Final reporting and error handling
```

#### State Flow

```
Validate Input
    ↓
Initialize E2E DB Record
    ↓
Compose Config
    ↓
Skip Env Setup Decision
    ├→ [Yes] Collect Commit Hashes
    └→ [No]  Trigger Environment Setup (with polling)
            ↓
         Collect Commit Hashes
    ↓
Operations Portal Tests
    ↓
Dry Run Decision
    ├→ [Yes] Success Path
    └→ [No]  Data Portal Website Pooler Init
            ↓
         Data Portal Website Pooler
            ↓
         Login Credentials Extraction
            ↓
         Data Portal Tests
            ↓
         Teardown Tests
            ↓
         Data Portal Website Teardown Pooler
            ↓
         Success Path

[Any Failure] → Failure Path (Database Update → Report → Failure)
```

#### Execution Parameters

To start a Step Functions execution, provide these input parameters:

- `OsduVersion` (string): OSDU version (e.g., r3m25)
- `EnterpriseProductTypeActive` (boolean): Enterprise product type flag
- `SkipEnvSetup` (boolean): Skip environment setup step
- `DataPortalAccountId` (string): Data Portal AWS account ID
- `DeploymentRoleName` (string): Data Portal IAM role name
- `DataPortalDomain` (string): Data Portal deployment URL
- `DataPortalHostedZoneId` (string): Route53 hosted zone ID
- `DryRun` (boolean): Run tests without triggering Data Portal deployment
- `TeardownTriggerActive` (boolean): Flag to trigger teardown tests
- `BackplaneTargetBranchName` (string): Backplane/Operations Portal repositories branch name for initial environment setup

**Example Payload:**
```json
{
  "OsduVersion": "r3m25",
  "EnterpriseProductTypeActive": true,
  "DataPortalAccountId": "018955241485",
  "DeploymentRoleName": "edi-e2e-tests-custom-fulfillment-role",
  "DataPortalDomain": "e2e-test-suite.edi.internal0.dataops.47lining.com",
  "DataPortalHostedZoneId": "Z03189402G93GYQF24E39",
  "DryRun": false,
  "SkipEnvSetup": true,
  "TeardownTriggerActive": true,
  "BackplaneTargetBranchName": "release/edi-enterprise-v1.2.1"
}
```

### S3 Resources for Test Reports

An S3 bucket stores all E2E test reports:

**Bucket**: `e2e_reports`

**Folders**:
- `operation_portal_subscription_test_reports/`
- `data_portal_verification_test_reports/`
- `data_portal_teardown_test_reports/`
- `final_reports/`

### Bitbucket OIDC Integration

The `bitbucket_permissions` module enables Bitbucket Pipelines to assume an AWS role via OIDC (no stored credentials).

#### Prerequisites

- AWS account with E2E tests deployed
- Bitbucket workspace access
- OpenSSL (for thumbprint extraction)

#### Required Variables

- `sfn_orchestrator_arn`: Step Functions orchestrator ARN
- `bitbucket_audience`: `ari:cloud:bitbucket::workspace/<WORKSPACE_UUID>`
- `bitbucket_oidc_provider_url`: `https://api.bitbucket.org/2.0/workspaces/47lining/pipelines-config/identity/oidc`
- `bitbucket_thumbprint`: SHA-1 thumbprint of Bitbucket's OIDC root certificate

#### Optional Variables

- `bitbucket_subjects`: List of allowed subjects (default: `["*"]`)
- `max_session_duration`: Session duration in seconds (default: 3600)

---

## CI/CD Pipeline

### Bitbucket Pipelines

The project uses Bitbucket Pipelines for CI/CD automation.

**Configuration**: `bitbucket-pipelines.yml`

### AWS CodeBuild

Multiple CodeBuild projects execute different test phases. All buildspec files are located in the `buildspecs/` directory:

- `buildspecs/buildspec-operations-portal.yml`: Operations Portal tests
- `buildspecs/buildspec-data-portal-verification.yml`: Data Portal verification tests
- `buildspecs/buildspec-data-portal-activation.yml`: Data Portal activation tests
- `buildspecs/buildspec-teardown.yml`: Teardown tests
- `buildspecs/buildspec.yml`: Main build specification

CodeBuild projects are provisioned by the main Terraform stack.

---

## Contributing

### Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following project conventions
   - Add/update tests as needed
   - Run quality checks locally

3. **Commit Changes**
   ```bash
   # Use Commitizen for structured commits
   cz commit
   cz bump
   ```

4. **Run Quality Checks**
   ```bash
   # Run all pre-commit hooks
   pre-commit run --all-files

   # Run tests
   make test
   make quality_test
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create a Pull Request to `main` branch
   - Ensure all CI checks pass

### Code Review Guidelines

- Follow the commit convention
- Ensure all tests pass
- Update documentation for new features
- Add tests for new functionality
- Keep changes focused and atomic

### Adding New Tests

#### E2E Tests

1. **Create test file** in appropriate portal folder:
   ```
   e2e/tests/operations_portal/feature/test_new_feature.py
   ```

2. **Add pytest marker**:
   ```python
   import pytest

   @pytest.mark.operations_portal
   def test_new_feature(op_page_unauth):
       # Test implementation
       pass
   ```

3. **Run locally**:
   ```bash
   pytest e2e/tests/operations_portal/feature/test_new_feature.py -v -m operations_portal
   ```

#### Unit Tests

1. **Create test file** in `tests/` directory matching source structure
2. **Follow pytest conventions**
3. **Run tests**:
   ```bash
   pytest tests -v
   ```

### Adding New Infrastructure

1. **Update Terraform Configuration**
   - Add resources to appropriate `.tf` file
   - Follow existing patterns and naming conventions

2. **Update State Machine** (if needed)
   - Modify relevant phase file in `definitions/`
   - Update state flow documentation

3. **Test Changes**
   ```bash
   terraform plan
   terraform apply
   ```

4. **Update Documentation**
   - Update relevant README files
   - Document new outputs and variables

### Version Bumping

```bash
# Interactive commit (auto-categorizes based on type)
cz commit

# Bump version (analyzes commits since last tag)
cz bump

# Push changes (DO NOT push tags automatically)
git push origin <branch>
```

---

## Troubleshooting

### Common Issues

#### Playwright Browser Launch Fails

**Symptom**: Browser fails to start in CI/CD

**Solution**:
```bash
# Ensure Playwright browsers are installed
playwright install

# In CI, use container with system dependencies
# or install dependencies: playwright install-deps
```

#### Test Fails with Missing Environment Variables

**Symptom**: `KeyError` or validation error for environment variable

**Solution**:
1. Check `e2e/example.env.test` for required variables
2. Update your local `.env.test` file
3. Verify fixture error message for specific missing variable

#### Pre-commit Hook Fails

**Symptom**: Commit rejected by pre-commit

**Solution**:
```bash
# Run hooks manually to see detailed errors
pre-commit run --all-files

# Fix issues
ruff check --fix .
ruff format .

# Retry commit
git commit -m "your message"
```

#### Terraform Build Fails: "command not found: sha256sum"

**Symptom**: Lambda build script fails on macOS

**Solution**:
```bash
# Install coreutils
brew install coreutils

# Or modify build_layer.sh to use shasum
shasum -a 256 <file>
```

#### Lambda Layer Size Too Large

**Symptom**: Layer exceeds 50MB compressed / 250MB uncompressed limit

**Solution**:
- Remove unnecessary dependencies from `requirements.txt`
- Use `--no-deps` for specific packages
- Split into multiple layers

#### Import Errors in Lambda

**Symptom**: `ModuleNotFoundError` in Lambda execution

**Solution**:
1. Ensure Lambda layer is attached to function
2. Verify Python runtime compatibility (3.13)
3. Check import path: `from shared import ...`

#### Terraform State Lock

**Symptom**: State file locked during `terraform apply`

**Solution**:
```bash
# Force unlock (use with caution)
terraform force-unlock <lock-id>
```

#### Route53 Hosted Zone Not Resolving

**Symptom**: Domain not resolving after Data Portal stack deployment

**Solution**:
1. Get NS records: `terraform output data_portal_route53_ns_records`
2. Update NS records at domain registrar
3. Allow time for DNS propagation (up to 48 hours)
4. Verify: `dig NS <your-domain>`

#### CodeBuild Test Failures

**Symptom**: Tests pass locally but fail in CodeBuild

**Solution**:
1. Check CloudWatch Logs for detailed error messages
2. Verify environment variables are set in CodeBuild project
3. Ensure secrets are accessible from CodeBuild IAM role
4. Test in headed mode locally to debug UI issues

---

## Additional Resources

### Documentation

- **Main README**: [README.md](README.md)
- **E2E Tests**: [e2e/README.md](e2e/README.md)
- **Bitbucket OIDC**: [infra/terraform/modules/bitbucket_permissions/README.md](infra/terraform/modules/bitbucket_permissions/README.md)
- **State Machine**: [infra/terraform/modules/test_execution_orchestrator/definitions/README.md](infra/terraform/modules/test_execution_orchestrator/definitions/README.md)

### External Links

- [Architecture & Docs E2E](https://47lining.atlassian.net/wiki/spaces/DataOps/pages/3892674613/EDI+E2E+tests+architecture+implementation)
- [HLD E2E](https://47lining.atlassian.net/wiki/spaces/DataOps/pages/3747971073/HLD+-+Automated+E2E+Testing+EDI)
- [ADR E2E](https://47lining.atlassian.net/wiki/spaces/DataOps/pages/3770875921/ADR+-+E2E+Implementation+concept)
- [Repo](https://bitbucket.org/47lining/edi-e2e-tests/src/main/)
- [JIRA](https://47lining.atlassian.net/browse/DATAOPS-10929)
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
