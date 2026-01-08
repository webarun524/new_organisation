# EDI Automated E2E Test Framework

This project manages infrastructure and e2e tests for EDI backplane infrastructure and deployment.
The project uses Poetry for dependency management and packaging, with a strict pre-commit workflow.

## Development Setup

### Environment Setup

```bash
# Python version is managed via .python-version (3.13)
poetry install --with dev
poetry shell
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

## Common Commands

### Code Quality

```bash
# Lint and auto-fix with Ruff
ruff check --fix .

# Format code
ruff format .

# Run both (via pre-commit)
pre-commit run --all-files
```

### Build scripts

The `buildscripts` directory contains helper scripts for building, deploying, and managing the E2E infrastructure and dependencies. Below is a list of all available scripts:

- `deploy.sh` – Deploys the E2E infrastructure to the target AWS account.
- `destroy.sh` – Destroys the deployed E2E infrastructure from the AWS account.
- `add_policy_for_approval_lambda.sh` – Grants the approval Lambda permission to subscribe to the SNS approval topic in the MB AWS account.
- `install-poetry.sh` – Installs Poetry for Python dependency management.
- `install-terraform.sh` – Installs Terraform for infrastructure provisioning.
- `quality.sh` – Runs quality checks and linting for the codebase.
- `add_ns_record_to_shared_data_portal_layer.sh` - Adds NS record to Route53 of shared services AWS account.

Refer to each script for usage details and required environment variables.

### Testing

#### Running E2E Tests Locally

```bash
# Activate the Poetry environment
poetry shell

# Install playwright if not done previously
playwright install

# Run with verbose output
pytest e2e_tests -v

# Run unit tests
pytest tests -v
```

#### Quick Test Run

```bash
# Without activating shell (runs in Poetry's virtual environment)
poetry run pytest -v
```

### Version Management

The project uses Commitizen for version bumping and changelog generation:

```bash
# Create a new commit (interactive)
cz commit

# Bump version based on commits
cz bump

# Current version is stored in VERSION file
```

Please ensure you do not push tags unintentionally by avoiding the `git push --tags` or `git push --follow-tags` commands. Be aware that GUI tools, such as GitHub Desktop, may automatically push local tags when you push your commits.

## Architecture

### Project Structure

- `src/edi_e2e_tests/`: Main package source code
- `tests/`: Test suite
- `scripts/`: Build and utility scripts
- `infra/`: Infrastructure as Code files

### Commit Convention

This project uses a custom Commitizen configuration with specific commit types:

- `feat`: New features (bumps MINOR version)
- `fix`: Bug fixes (bumps PATCH version)
- `chore`: Maintenance tasks (bumps PATCH version)
- `bump`: Version bump commits
- `revert`: Reverts previous commits (bumps PATCH version)

Commits must follow the pattern: `<type>: <message>` with optional context, JIRA ticket, and breaking change information.

### Code Quality Configuration

- **Ruff**: Configured for line length 88, target Python 3.10+ syntax
- **Pre-commit**: Enforces trailing whitespace removal, end-of-file fixing, YAML validation, large file checks, Ruff linting/formatting, and Terraform formatting (for future infrastructure code)

### Linting Rules

The project uses Ruff with the following enabled:

- E (Error rules)
- F (Pyflakes)
- W (Warning rules)
- I (isort for import sorting)

Exception: E501 (line too long) is ignored as the formatter handles this.

## Package Details

- Package name: `edi-e2e-tests`
- Package location: `src/edi_e2e_tests`
- Requires Python: >=3.13,<4.0
- Build system: Poetry Core (>=2.0.0,<3.0.0)

## Infrastructure

The project contains two Terraform stacks:

- `infra/terraform`: the main E2E infrastructure stack. It provisions core resources used during test execution (Lambda functions, shared Lambda layer, CodeBuild projects, Step Functions, DynamoDB tables, IAM roles, S3 buckets for artifacts and reports, etc.).
- `infra/data_portal/terraform`: a smaller, auxiliary stack that provisions Data Portal specific resources such as a Route53 hosted zone and helper IAM role/policy used for Data Portal custom fulfillment and DNS delegation.

Deployment order

When deploying these stacks for a new environment, follow this order to ensure required permissions and resources exist before dependent steps run:

1. `buildscripts/add_policy_for_approval_lambda.sh` — run this first to ensure the approval Lambda has the necessary SNS subscription permissions in any target accounts that require cross-account subscriptions.
2. `infra/terraform` — deploy the primary E2E infrastructure (Lambda functions, CodeBuild, Step Function state machine, reporting resources, etc.). This stack creates the CodeBuild projects and other resources that may reference or depend on the Data Portal outputs.
3. `infra/data_portal/terraform` — deploy the Data Portal helper stack that creates the Route53 hosted zone and custom fulfillment IAM role/policy. The hosted zone NS records will be needed for DNS delegation.
4. `buildscripts/add_policy_for_approval_lambda.sh` — run the approval Lambda permission script again (if applicable) to ensure the approval Lambda has up-to-date permissions after both stacks are created (some permission boundaries or ARNs may have changed after deployment).

Notes

- The second pass of `add_policy_for_approval_lambda.sh` is optional in many setups; run it if your deployment requires the approval Lambda to subscribe to SNS topics or resources created during the Terraform deployment.
- After creating the hosted zone in `infra/data_portal/terraform`, update your registrar to delegate the domain using the NS records exported by the stack.
- Always run `terraform plan` before `apply` to review changes.

Terraform formatting is already configured in pre-commit hooks.

## S3 Resources for Test Reports

An S3 bucket is provisioned to store all E2E test reports and integrate with AWS CodeBuild and the final reporting workflow
Bucket: e2e_reports

Folders:

`operation_portal_subscription_test_reports/`
`data_portal_verification_test_reports/`
`data_portal_teardown_test_reports/`
`final_reports/`

## Makefile Help

Each MB repository implements makefile scripts which use uniform interface of commands.
Execute following command to get information about supported make commands.

```shell
make help

help:                     	Display this help message.
install:                  	Installs Python dependencies.
test:                     	Runs unit tests.
quality_test:             	Runs quality checks.
e2e_op_tests:             	Runs end-to-end tests for the Operations Portal.
e2e_dp_verification_tests:  Runs end-to-end tests for Data Portal verification.
e2e_dp_teardown_tests:  	  Runs end-to-end tests for Data Portal teardown.
build:                  	  Builds application.
deploy:                 	  Deploys application.
destroy:                	  Destroys application.
```
