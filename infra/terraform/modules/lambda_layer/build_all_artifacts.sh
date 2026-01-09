#!/bin/bash
set -euxo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting build of all resources at $(date)${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Build Lambda Layer
echo -e "${YELLOW}Building Lambda layer...${NC}"
./build_layer.sh
echo -e "${GREEN}✓ Lambda layer build completed.${NC}"

# Define Lambda Functions
LAMBDA_FUNCTIONS=(approval_handler commit_collector execution_record_handler reporter config_composer deployment_checker setup_trigger execution_params_validator dp_password_rotator deployment_data_extractor)

# Build Lambda Functions
for fn in "${LAMBDA_FUNCTIONS[@]}"; do
  echo -e "${YELLOW}Building Lambda function: $fn${NC}"
  ./build_lambda.sh "$fn"
  echo -e "${GREEN}✓ Lambda function $fn build completed.${NC}"
done

echo -e "${GREEN}✓ All resources built successfully at $(date)${NC}"
