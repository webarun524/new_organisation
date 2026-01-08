#!/usr/bin/env bash
set -euxo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}Running Quality checks...${NC}"

echo -e "\n${YELLOW}Setting Variables...${NC}"
export TF_PATH="$(pwd)/infra/terraform"
export POETRY_HOME=/root/.local
export PATH="$POETRY_HOME/bin:$PATH"

echo -e "\n${YELLOW}Run pre-commit checks...${NC}"
# disable terraform_validate in the CI, takes too long on the first run
SKIP="terraform_validate,terraform_tflint" poetry run pre-commit run --all-files

echo -e "\n${YELLOW}Outdated packages:${NC}"
poetry show -oT

echo -e "\n${YELLOW}Running terraform validate...${NC}"
cd "$TF_PATH"
terraform init -backend="false"
terraform validate

echo -e "\n${YELLOW}Running tflint...${NC}"
tflint
