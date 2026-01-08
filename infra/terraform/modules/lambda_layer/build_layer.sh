#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building Lambda Layer...${NC}"

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
BUILD_DIR="$SCRIPT_DIR/../../build/layer_build"
LAYER_DIR="$BUILD_DIR/python"
echo -e "${YELLOW}SCRIPT_DIR-${SCRIPT_DIR}"
echo -e "${YELLOW}PROJECT_ROOT${PROJECT_ROOT}"
echo -e "${YELLOW}BUILD_DIR-${BUILD_DIR}"
echo -e "${YELLOW}LAYER_DIR${LAYER_DIR}"

# Clean up previous build
echo -e "${YELLOW}Cleaning up previous build...${NC}"
rm -rf "$LAYER_DIR"
rm -f "$BUILD_DIR/lambda_layer.zip"
rm -f "$BUILD_DIR/layer_hash.txt"
mkdir -p "$LAYER_DIR"

# Copy shared modules to layer
echo -e "${YELLOW}Copying shared modules...${NC}"
if [ -d "$PROJECT_ROOT/src/shared" ]; then
    cp -r "$PROJECT_ROOT/src/shared" "$LAYER_DIR/"
    echo -e "${GREEN}✓ Copied shared modules${NC}"
else
    echo -e "${RED}✗ Error: src/shared directory not found${NC}"
    exit 1
fi

# Extract python version
if [ ! -f "$PROJECT_ROOT/.python-version" ]; then
    echo -e "${RED}✗ Error: .python-version file not found in project root${NC}"
    exit 1
fi
PYTHON_VERSION="$(cat "$PROJECT_ROOT/.python-version" 2>/dev/null)"
echo -e "${YELLOW}Using Python version: ${PYTHON_VERSION}${NC}"

# Install Python dependencies from requirements.txt
if [ -f "$PROJECT_ROOT/src/shared/requirements.txt" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install \
        --platform manylinux2014_x86_64 \
        --target="$LAYER_DIR" \
        --implementation cp \
        --python-version "$PYTHON_VERSION" \
        --only-binary=:all: \
        --upgrade \
        -r "$PROJECT_ROOT/src/shared/requirements.txt"

    echo -e "${GREEN}✓ Installed dependencies${NC}"
else
    echo -e "${YELLOW}⚠ No requirements.txt found, skipping dependency installation${NC}"
fi

# Remove unnecessary files to reduce size
echo -e "${YELLOW}Cleaning up layer files...${NC}"
find "$LAYER_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$LAYER_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$LAYER_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$LAYER_DIR" -name "*.pyc" -delete 2>/dev/null || true
find "$LAYER_DIR" -name "*.pyo" -delete 2>/dev/null || true

# Create ZIP file
echo -e "${YELLOW}Creating layer ZIP file...${NC}"
cd "$BUILD_DIR"
zip -r9 lambda_layer.zip python > /dev/null
cd "$SCRIPT_DIR"

# Calculate hash for tracking changes
LAYER_HASH=$(sha256sum "$BUILD_DIR/lambda_layer.zip" | cut -d' ' -f1)
echo "$LAYER_HASH" > "$BUILD_DIR/layer_hash.txt"
echo -e "${GREEN}✓ Layer hash: $LAYER_HASH${NC}"

echo -e "${GREEN}Lambda Layer build complete!${NC}"
