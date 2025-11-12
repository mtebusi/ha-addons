#!/usr/bin/env bash
# Shared build script for Home Assistant add-ons
# Usage: ./build.sh <addon-directory> [--arch <architecture>] [--push]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PUSH=false
ARCH="amd64"
REGISTRY="ghcr.io"

# Parse arguments
ADDON_DIR=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --arch)
            ARCH="$2"
            shift 2
            ;;
        --push)
            PUSH=true
            shift
            ;;
        --registry)
            REGISTRY="$2"
            shift 2
            ;;
        *)
            if [ -z "$ADDON_DIR" ]; then
                ADDON_DIR="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$ADDON_DIR" ]; then
    echo -e "${RED}Error: No addon directory specified${NC}"
    echo "Usage: $0 <addon-directory> [--arch <architecture>] [--push] [--registry <registry>]"
    exit 1
fi

if [ ! -d "$ADDON_DIR" ]; then
    echo -e "${RED}Error: Addon directory '$ADDON_DIR' does not exist${NC}"
    exit 1
fi

if [ ! -f "$ADDON_DIR/config.yaml" ]; then
    echo -e "${RED}Error: No config.yaml found in '$ADDON_DIR'${NC}"
    exit 1
fi

# Extract addon information
ADDON_NAME=$(grep "^name:" "$ADDON_DIR/config.yaml" | cut -d'"' -f2)
ADDON_VERSION=$(grep "^version:" "$ADDON_DIR/config.yaml" | cut -d'"' -f2)
ADDON_SLUG=$(grep "^slug:" "$ADDON_DIR/config.yaml" | awk '{print $2}')

echo -e "${GREEN}Building addon: $ADDON_NAME${NC}"
echo -e "Version: $ADDON_VERSION"
echo -e "Architecture: $ARCH"
echo -e "Slug: $ADDON_SLUG"

# Determine base image
case "$ARCH" in
    amd64)   BASE_IMAGE="ghcr.io/home-assistant/amd64-base:latest" ;;
    aarch64) BASE_IMAGE="ghcr.io/home-assistant/aarch64-base:latest" ;;
    armhf)   BASE_IMAGE="ghcr.io/home-assistant/armhf-base:latest" ;;
    armv7)   BASE_IMAGE="ghcr.io/home-assistant/armv7-base:latest" ;;
    i386)    BASE_IMAGE="ghcr.io/home-assistant/i386-base:latest" ;;
    *)
        echo -e "${RED}Error: Unsupported architecture '$ARCH'${NC}"
        exit 1
        ;;
esac

# Build image
IMAGE_NAME="$REGISTRY/$GITHUB_REPOSITORY_OWNER/${ARCH}-${ADDON_SLUG}"
if [ -z "$GITHUB_REPOSITORY_OWNER" ]; then
    # Fallback for local builds
    IMAGE_NAME="$REGISTRY/local/${ARCH}-${ADDON_SLUG}"
fi

echo -e "${YELLOW}Building Docker image...${NC}"
docker buildx build \
    --platform "linux/$ARCH" \
    --build-arg "BUILD_FROM=$BASE_IMAGE" \
    --build-arg "BUILD_ARCH=$ARCH" \
    --build-arg "BUILD_VERSION=$ADDON_VERSION" \
    --build-arg "BUILD_NAME=$ADDON_NAME" \
    --build-arg "BUILD_DESCRIPTION=$ADDON_NAME" \
    --tag "$IMAGE_NAME:latest" \
    --tag "$IMAGE_NAME:$ADDON_VERSION" \
    "$ADDON_DIR"

if [ "$PUSH" = true ]; then
    echo -e "${YELLOW}Pushing image to registry...${NC}"
    docker push "$IMAGE_NAME:latest"
    docker push "$IMAGE_NAME:$ADDON_VERSION"
    echo -e "${GREEN}Push complete!${NC}"
fi

echo -e "${GREEN}Build complete!${NC}"
echo -e "Image: $IMAGE_NAME:$ADDON_VERSION"
