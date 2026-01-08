#!/usr/bin/env bash
set -euxo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Required Environment Variables
: "${AWS_REGION:?Required environment variable not set}"
: "${TERRAFORM_BUCKET:?Required environment variable not set}"
: "${BACKPLANE_ACCOUNT_ID:?Required environment variable not set}"
: "${BITBUCKET_TOKEN:?Required environment variable not set}"
: "${DEPLOYMENT_ENVIRONMENT_CODE:?Required environment variable not set}"

# Optional Environment Variables with Defaults
export TF_VAR_aws_region="${TF_VAR_aws_region:-$AWS_REGION}"
export TF_VAR_deployment_environment_code="${TF_VAR_deployment_environment_code:-$DEPLOYMENT_ENVIRONMENT_CODE}"
export TF_VAR_bitbucket_token="${TF_VAR_bitbucket_token:-$BITBUCKET_TOKEN}"
export TF_VAR_backplane_account_id="${TF_VAR_backplane_account_id:-$BACKPLANE_ACCOUNT_ID}"

# Display Configuration
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Terraform Deployment Configuration${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}AWS Region:${NC}             ${TF_VAR_aws_region}"
echo -e "${YELLOW}Deployment Environment Code:${NC} ${TF_VAR_deployment_environment_code}"
echo -e "${YELLOW}Bitbucket Token:${NC}        ${TF_VAR_bitbucket_token}"
echo -e "${YELLOW}Backplane Account ID:${NC}   ${TF_VAR_backplane_account_id}"
echo -e "${YELLOW}S3 Backend Bucket:${NC}      ${TERRAFORM_BUCKET}"
echo -e "${BLUE}========================================${NC}"

# Get script directory and navigate to infrastructure
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT/infra/terraform"

echo -e "\n${YELLOW}Checking Terraform version...${NC}"
terraform --version

# Terraform Init
echo -e "\n${YELLOW}Initializing Terraform...${NC}"
terraform init \
    -reconfigure \
    -backend-config="region=${AWS_REGION}" \
    -backend-config="bucket=${TERRAFORM_BUCKET}" \
    -backend="true"

echo -e "\n${YELLOW}Destroying Terraform configuration...${NC}"
terraform destroy -auto-approve
