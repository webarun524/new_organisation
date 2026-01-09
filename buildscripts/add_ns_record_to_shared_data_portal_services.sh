#!/usr/bin/env bash
set -euxo pipefail

# ===============================
# Example usage
# ===============================
#   $ export DOMAIN_NAME="e2e-test-suite.edi.internal0.dataops.47lining.com"
#   $ export RECORD_NS_VALUE=$'ns-592.awsdns-10.net.\nns-1327.awsdns-37.org.\nns-1856.awsdns-40.co.uk.\nns-490.awsdns-61.com.'
#   # login to `126748958625` AWS account where the shared hosted zone is located
#   $ ./add_ns_record_to_shared_data_portal_services.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ===============================
# Environment Variables
# ===============================
: "${DOMAIN_NAME:?Environment variable DOMAIN_NAME is required but not set}"
: "${RECORD_NS_VALUE:?Environment variable RECORD_NS_VALUE is required but not set}"

# Optional with default
HOSTED_ZONE_ID="${HOSTED_ZONE_ID:-Z10284071LNCA50Q5DXM9}"

# ===============================
# Check AWS CLI availability
# ===============================
echo -e "\n${YELLOW}Checking AWS CLI availability...${NC}"
if ! command -v aws >/dev/null 2>&1; then
    echo -e "${RED}✗ Error: AWS CLI is not installed or not available in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✓ AWS CLI found${NC}"
aws --version

# ===============================
# Display Configuration
# ===============================
echo -e "${BLUE}===============================${NC}"
echo -e "${BLUE}Configuration${NC}"
echo -e "${BLUE}===============================${NC}"
echo -e "${YELLOW}Domain Name:${NC}           ${DOMAIN_NAME}"
echo -e "${YELLOW}NS Record Value:${NC}       ${RECORD_NS_VALUE}"
echo -e "${YELLOW}Hosted Zone ID:${NC}        ${HOSTED_ZONE_ID}"
echo -e "${BLUE}===============================${NC}"

# ===============================
# Create Route 53 Change Batch JSON
# ===============================
echo -e "\n${YELLOW}Creating Route 53 NS record change batch...${NC}"

# Convert RECORD_NS_VALUE (possibly multiline) into JSON array entries
RESOURCE_RECORDS_JSON=$(printf "%s" "${RECORD_NS_VALUE}" | sed '/^[[:space:]]*$/d' | awk '{printf "{ \"Value\": \"%s\" },", $0}' | sed 's/,$//')

CHANGE_BATCH=$(cat <<EOF
{
  "Comment": "Create NS record for ${DOMAIN_NAME}",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "${DOMAIN_NAME}",
        "Type": "NS",
        "TTL": 300,
        "ResourceRecords": [
          ${RESOURCE_RECORDS_JSON}
        ]
      }
    }
  ]
}
EOF
)

# Validate JSON
if ! echo "${CHANGE_BATCH}" | python3 -m json.tool > /dev/null 2>&1; then
    echo -e "${RED}✗ Error: Generated Route 53 JSON is invalid${NC}"
    exit 1
fi
echo -e "${GREEN}✓ JSON validated${NC}"

# ===============================
# Apply DNS change via Route 53
# ===============================
echo -e "\n${YELLOW}Submitting Route 53 change request...${NC}"

aws route53 change-resource-record-sets \
  --hosted-zone-id "${HOSTED_ZONE_ID}" \
  --change-batch "${CHANGE_BATCH}"

echo -e "\n${GREEN}✓ Success! Route 53 NS record created/updated${NC}"
