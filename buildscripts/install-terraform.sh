#!/bin/bash
set -euxo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}Installing Terraform and TFLint${NC}"

TERRAFORM_VERSION="${TERRAFORM_VERSION:-1.13.4}"
TFLINT_VERSION="${TFLINT_VERSION:-0.55.0}"

# Ensure jq, unzip & curl is installed
echo -e "\n${YELLOW}Installing jq...${NC}"
if ! command -v jq &>/dev/null; then
  echo "jq not found — installing..."
  if command -v apt-get &>/dev/null; then
    apt-get update -y
    apt-get install -y jq unzip curl
  elif command -v apk &>/dev/null; then
    apk add --no-cache jq unzip curl
  elif command -v yum &>/dev/null; then
    yum install -y jq unzip curl
  else
    echo "Could not install jq automatically (unsupported package manager)." >&2
    exit 1
  fi
fi

# Check if terraform is already installed with the correct version
echo -e "\n${YELLOW}Checking Terraform installation...${NC}"
if command -v terraform &> /dev/null; then
  if terraform version -json >/dev/null 2>&1; then
    INSTALLED_VERSION=$(terraform version -json | jq -r .terraform_version)
  else
    INSTALLED_VERSION=$(terraform version | head -n1 | awk '{print $2}' | tr -d 'v')
  fi
  if [ "$(printf '%s\n' "$INSTALLED_VERSION" "$TERRAFORM_VERSION" | sort -V | tail -n1)" != "$INSTALLED_VERSION" ]; then
    echo "Installed Terraform ($INSTALLED_VERSION) is older than required ($TERRAFORM_VERSION). Installing..."
  else
    echo "Terraform $INSTALLED_VERSION is already sufficient"
  fi
else
  echo "Terraform not found. Installing version $TERRAFORM_VERSION..."
fi

echo -e "\n${YELLOW}Downloading and installing Terraform...${NC}"
curl -sSL -o terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"

if [ -n "${BITBUCKET_BUILD_NUMBER+x}" ]; then
  unzip -o terraform.zip -d ~/.local/bin
else
  unzip -o terraform.zip -d terraform
  tf_path="$(pwd)/terraform"
  chmod +x "$tf_path"/terraform
  export PATH="${tf_path}:$PATH"
fi

echo -e "\n${GREEN}Terraform $TERRAFORM_VERSION installed successfully${NC}"

echo -e "\n${YELLOW}Checking TFLint installation...${NC}"
if command -v tflint &> /dev/null; then
  INSTALLED_TFLINT_VERSION=$(tflint --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n1)
  if [ "$(printf '%s\n' "$INSTALLED_TFLINT_VERSION" "$TFLINT_VERSION" | sort -V | tail -n1)" != "$INSTALLED_TFLINT_VERSION" ]; then
    echo "Installed TFLint ($INSTALLED_TFLINT_VERSION) is older than required ($TFLINT_VERSION). Installing..."
  else
    echo "TFLint $INSTALLED_TFLINT_VERSION is already sufficient"
    exit 0
  fi
else
  echo "TFLint not found. Installing version $TFLINT_VERSION..."
fi

echo -e "\n${YELLOW}Downloading and installing TFLint...${NC}"
curl -sSL -o tflint.zip "https://github.com/terraform-linters/tflint/releases/download/v${TFLINT_VERSION}/tflint_linux_amd64.zip"

if [ -n "${BITBUCKET_BUILD_NUMBER+x}" ]; then
  unzip -o tflint.zip -d ~/.local/bin
else
  unzip -o tflint.zip -d tflint
  tf_path="$(pwd)/tflint"
  chmod +x "$tf_path"/tflint
  export PATH="${tf_path}:$PATH"
fi

echo -e "\n${GREEN}TFLint $TFLINT_VERSION installed successfully${NC}"
