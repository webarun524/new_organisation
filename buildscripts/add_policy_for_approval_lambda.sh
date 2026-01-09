#!/usr/bin/env bash
set -euxo pipefail

# ===============================
# Example usage
# ===============================
#   $ export AWS_REGION="us-east-1"
#   $ export SNS_ARN="arn:aws:sns:us-east-1:123456789012:my-approval-topic"
#   $ export E2E_AWS_HOST="123456789012"
#   # login to Operations Portal AWS account where SNS is located
#   $ ./add_policy_for_approval_lambda.sh


# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Required Environment Variables
: "${AWS_REGION:?Required environment variable not set}"
: "${SNS_ARN:?Required environment variable not set}"
: "${E2E_AWS_HOST:?Required environment variable not set}"

echo -e "\n${YELLOW}Checking AWS CLI version...${NC}"
aws --version

# Display Configuration
echo -e "${BLUE}===============================${NC}"
echo -e "${BLUE}Configuration${NC}"
echo -e "${BLUE}===============================${NC}"
echo -e "${YELLOW}AWS Region:${NC}             ${AWS_REGION}"
echo -e "${YELLOW}SNS topic ARN:${NC}          ${SNS_ARN}"
echo -e "${YELLOW}E2E Account number:${NC}     ${E2E_AWS_HOST}"
echo -e "${BLUE}===============================${NC}"

# Create SNS policy JSON
echo -e "\n${YELLOW}Creating SNS policy...${NC}"
POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowYourAccountToSubscribe",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${E2E_AWS_HOST}:root"
      },
      "Action": "sns:Subscribe",
      "Resource": "${SNS_ARN}"
    }
  ]
}
EOF
)

# Validate JSON
if ! echo "${POLICY}" | python3 -m json.tool > /dev/null 2>&1; then
    echo -e "${RED}✗ Error: Generated policy is not valid JSON${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Policy JSON validated${NC}"

# Add allow policy to SNS topic on mb account
echo -e "\n${YELLOW}Adding Allow Policy to subscribe to SNS topic for approval lambda...${NC}"
aws sns set-topic-attributes \
  --topic-arn "${SNS_ARN}" \
  --attribute-name Policy \
  --attribute-value "${POLICY}" \
  --region "${AWS_REGION}"

echo -e "\n${GREEN}✓ Success! SNS policy updated${NC}"
