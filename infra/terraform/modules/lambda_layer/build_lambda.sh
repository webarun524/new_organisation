#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building Lambda Function...${NC}"

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
BUILD_DIR="$SCRIPT_DIR/../../build/layer_build"
LAYER_DIR="$BUILD_DIR/python"
echo -e "${YELLOW}SCRIPT_DIR-${SCRIPT_DIR}"
echo -e "${YELLOW}PROJECT_ROOT${PROJECT_ROOT}"
echo -e "${YELLOW}BUILD_DIR-${BUILD_DIR}"
echo -e "${YELLOW}LAYER_DIR${LAYER_DIR}"
LAMBDA_NAME="$1"

if [ -z "$LAMBDA_NAME" ]; then
    echo -e "${RED}✗ Error: Lambda name not provided${NC}"
    echo "Usage: ./build_lambda.sh <lambda_name>"
    exit 1
fi

LAMBDA_SOURCE="$PROJECT_ROOT/src/lambdas/$LAMBDA_NAME"

if [ ! -d "$LAMBDA_SOURCE" ]; then
    echo -e "${RED}✗ Error: Lambda source directory not found: $LAMBDA_SOURCE${NC}"
    exit 1
fi

# Clean up previous build
echo -e "${YELLOW}Cleaning up previous build...${NC}"
rm -rf "$BUILD_DIR/lambdas/$LAMBDA_NAME"

# Copy Lambda function code with proper package structure
echo -e "${YELLOW}Copying Lambda function code...${NC}"

# Create the lambdas package structure
mkdir -p "$BUILD_DIR/lambdas/$LAMBDA_NAME"

# Copy the lambdas __init__.py if it exists
if [ -f "$PROJECT_ROOT/src/lambdas/__init__.py" ]; then
    cp "$PROJECT_ROOT/src/lambdas/__init__.py" "$BUILD_DIR/lambdas/"
else
    # Create empty __init__.py if it doesn't exist
    touch "$BUILD_DIR/lambdas/__init__.py"
fi

# Copy the Lambda function code
cp -r "$LAMBDA_SOURCE"/* "$BUILD_DIR/lambdas/$LAMBDA_NAME/"

# Remove unnecessary files
echo -e "${YELLOW}Cleaning up Lambda files...${NC}"
find "$BUILD_DIR/lambdas" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR/lambdas" -name "*.pyc" -delete 2>/dev/null || true
find "$BUILD_DIR/lambdas" -name "*.pyo" -delete 2>/dev/null || true
find "$BUILD_DIR/lambdas" -name ".DS_Store" -delete 2>/dev/null || true

# Create ZIP file
echo -e "${YELLOW}Creating Lambda ZIP file...${NC}"
cd "$BUILD_DIR"
zip -r9 "${LAMBDA_NAME}.zip" lambdas/${LAMBDA_NAME} > /dev/null

# Get ZIP file size
ZIP_SIZE=$(du -h "$BUILD_DIR/${LAMBDA_NAME}.zip" | cut -f1)
echo -e "${GREEN}✓ Lambda ZIP created: $BUILD_DIR/${LAMBDA_NAME}.zip ($ZIP_SIZE)${NC}"

# Calculate hash for tracking changes
LAMBDA_HASH=$(shasum -a 256 "$BUILD_DIR/${LAMBDA_NAME}.zip" | cut -d' ' -f1)
echo "$LAMBDA_HASH" > "$BUILD_DIR/${LAMBDA_NAME}_hash.txt"
echo -e "${GREEN}✓ Lambda hash: $LAMBDA_HASH${NC}"

echo -e "${GREEN}Lambda build complete!${NC}"
