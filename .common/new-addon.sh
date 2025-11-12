#!/usr/bin/env bash
# Quick-start script for creating a new Home Assistant add-on
# Usage: ./.common/new-addon.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Home Assistant Add-on Quick-Start Generator              ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Check if we're in the repository root
if [ ! -d ".common" ] || [ ! -f "repository.json" ]; then
    echo -e "${RED}❌ Error: This script must be run from the repository root${NC}"
    echo -e "${YELLOW}   cd to your ha-addons directory and run: ./.common/new-addon.sh${NC}"
    exit 1
fi

# Prompt for add-on details
echo -e "${BLUE}Let's create your new add-on!${NC}"
echo ""

# Add-on name
read -p "📝 Add-on name (e.g., 'My Awesome Service'): " ADDON_NAME
if [ -z "$ADDON_NAME" ]; then
    echo -e "${RED}❌ Add-on name cannot be empty${NC}"
    exit 1
fi

# Generate slug from name (lowercase, replace spaces with hyphens)
DEFAULT_SLUG=$(echo "$ADDON_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
read -p "🔖 Add-on slug (default: ${DEFAULT_SLUG}): " ADDON_SLUG
ADDON_SLUG=${ADDON_SLUG:-$DEFAULT_SLUG}

# Check if directory already exists
if [ -d "$ADDON_SLUG" ]; then
    echo -e "${RED}❌ Directory '$ADDON_SLUG' already exists!${NC}"
    exit 1
fi

# Description
read -p "📋 Brief description: " ADDON_DESCRIPTION
if [ -z "$ADDON_DESCRIPTION" ]; then
    ADDON_DESCRIPTION="A Home Assistant add-on"
fi

# Port
read -p "🌐 Main port (default: 8080): " ADDON_PORT
ADDON_PORT=${ADDON_PORT:-8080}

# Language choice
echo ""
echo -e "${BLUE}Select your programming language:${NC}"
echo "  1) Python"
echo "  2) Node.js"
echo "  3) Bash/Shell"
echo "  4) Other (manual setup)"
read -p "Choice (1-4, default: 1): " LANG_CHOICE
LANG_CHOICE=${LANG_CHOICE:-1}

case $LANG_CHOICE in
    1) LANGUAGE="python" ;;
    2) LANGUAGE="nodejs" ;;
    3) LANGUAGE="bash" ;;
    4) LANGUAGE="other" ;;
    *) LANGUAGE="python" ;;
esac

echo ""
echo -e "${GREEN}📦 Creating add-on structure...${NC}"

# Create directory structure
mkdir -p "$ADDON_SLUG"
mkdir -p "$ADDON_SLUG/rootfs/app"
mkdir -p "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}"

# Create config.yaml
cat > "$ADDON_SLUG/config.yaml" << EOF
name: "$ADDON_NAME"
version: "0.1.0"
slug: "$ADDON_SLUG"
description: "$ADDON_DESCRIPTION"
url: "https://github.com/mtebusi/ha-addons"
arch:
  - amd64
  - aarch64
  - armhf
  - armv7
  - i386
startup: services
boot: auto
init: false
hassio_api: true
homeassistant_api: true
auth_api: false
ports:
  ${ADDON_PORT}/tcp: ${ADDON_PORT}
ports_description:
  ${ADDON_PORT}/tcp: "Web interface"
options:
  log_level: info
schema:
  log_level: list(debug|info|warning|error)
image: "ghcr.io/mtebusi/{arch}-${ADDON_SLUG}"
EOF

# Create Dockerfile based on language
if [ "$LANGUAGE" = "python" ]; then
    cat > "$ADDON_SLUG/Dockerfile" << 'EOF'
ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/sh", "-c"]

# Setup base system and Python
RUN \
    apk add --no-cache \
        python3 \
        py3-pip

# Copy root filesystem (includes app code in /app)
COPY rootfs /

# Install Python dependencies
RUN \
    if [ -f /app/requirements.txt ]; then \
        python3 -m pip install --no-cache-dir --break-system-packages -r /app/requirements.txt && \
        rm -f /app/requirements.txt; \
    fi

# Set working directory
WORKDIR /app

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="mtebusi <mtebusi@example.com>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="HomeAssistant Add-ons" \
    org.opencontainers.image.authors="mtebusi <mtebusi@example.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/mtebusi/ha-addons" \
    org.opencontainers.image.source="https://github.com/mtebusi/ha-addons" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
EOF

    # Create requirements.txt
    cat > "$ADDON_SLUG/rootfs/app/requirements.txt" << EOF
# Add your Python dependencies here
# Example:
# flask==3.0.0
# requests==2.31.0
EOF

    # Create main.py
    cat > "$ADDON_SLUG/rootfs/app/main.py" << EOF
#!/usr/bin/env python3
"""
${ADDON_NAME}
"""
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    logger.info("Starting ${ADDON_NAME}...")

    # TODO: Implement your add-on logic here

    logger.info("${ADDON_NAME} is running!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
EOF

    chmod +x "$ADDON_SLUG/rootfs/app/main.py"

    # Create service run script
    cat > "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/run" << EOF
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start ${ADDON_NAME}
# ==============================================================================
bashio::log.info "Starting ${ADDON_NAME}..."

cd /app
exec python3 -u main.py
EOF

elif [ "$LANGUAGE" = "nodejs" ]; then
    cat > "$ADDON_SLUG/Dockerfile" << 'EOF'
ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/sh", "-c"]

# Setup base system and Node.js
RUN \
    apk add --no-cache \
        nodejs \
        npm

# Copy root filesystem
COPY rootfs /

# Install Node.js dependencies
RUN \
    if [ -f /app/package.json ]; then \
        cd /app && npm install --production && \
        rm -rf /tmp/*; \
    fi

# Set working directory
WORKDIR /app

# Build arguments and labels (same as Python)
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION}
EOF

    # Create package.json
    cat > "$ADDON_SLUG/rootfs/app/package.json" << EOF
{
  "name": "$ADDON_SLUG",
  "version": "0.1.0",
  "description": "$ADDON_DESCRIPTION",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {}
}
EOF

    # Create index.js
    cat > "$ADDON_SLUG/rootfs/app/index.js" << EOF
/**
 * ${ADDON_NAME}
 */
console.log('Starting ${ADDON_NAME}...');

// TODO: Implement your add-on logic here

console.log('${ADDON_NAME} is running!');
EOF

    # Create service run script
    cat > "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/run" << EOF
#!/usr/bin/with-contenv bashio
bashio::log.info "Starting ${ADDON_NAME}..."

cd /app
exec node index.js
EOF

else
    # Basic Dockerfile for other languages
    cp .common/templates/Dockerfile.template "$ADDON_SLUG/Dockerfile"

    # Basic run script
    cat > "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/run" << EOF
#!/usr/bin/with-contenv bashio
bashio::log.info "Starting ${ADDON_NAME}..."

cd /app
# TODO: Add your startup command here
exec /bin/sleep infinity
EOF
fi

# Make run script executable
chmod +x "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/run"

# Create finish script
cat > "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/finish" << 'EOF'
#!/usr/bin/execlineb -S0
# ==============================================================================
# Take down the S6 supervision tree when service fails
# ==============================================================================
if { s6-test ${1} -ne 0 }
if { s6-test ${1} -ne 256 }

s6-svscanctl -t /var/run/s6/services
EOF

chmod +x "$ADDON_SLUG/rootfs/etc/services.d/${ADDON_SLUG}/finish"

# Create README.md
cat > "$ADDON_SLUG/README.md" << EOF
# $ADDON_NAME

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

## About

$ADDON_DESCRIPTION

## Installation

1. Add this repository to your Home Assistant instance:
   - Navigate to **Supervisor** → **Add-on Store** → **⋮** → **Repositories**
   - Add: \`https://github.com/mtebusi/ha-addons\`
2. Install the "$ADDON_NAME" add-on
3. Configure the add-on (see Configuration section)
4. Start the add-on
5. Check the logs to see if everything is working

## Configuration

\`\`\`yaml
log_level: info
\`\`\`

### Option: \`log_level\`

The \`log_level\` option controls the level of log output.

- \`debug\`: Shows detailed debug information
- \`info\`: Normal informational messages
- \`warning\`: Warning messages only
- \`error\`: Error messages only

## Usage

TODO: Add usage instructions

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/mtebusi/ha-addons/issues).

## License

MIT License - see [LICENSE](../LICENSE) for details.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
EOF

# Create DOCS.md
cat > "$ADDON_SLUG/DOCS.md" << EOF
# $ADDON_NAME Documentation

## Installation

Follow the standard Home Assistant add-on installation process.

## Configuration

All configuration options are available in the add-on configuration panel.

## Usage

TODO: Add detailed usage instructions

## Troubleshooting

If you encounter issues:

1. Check the add-on logs for errors
2. Verify your configuration is correct
3. Ensure your Home Assistant version is compatible
4. Report issues on GitHub

## Support

For help and support:
- GitHub Issues: https://github.com/mtebusi/ha-addons/issues
- Home Assistant Community: https://community.home-assistant.io/
EOF

# Create CHANGELOG.md
cat > "$ADDON_SLUG/CHANGELOG.md" << EOF
# Changelog

All notable changes to this add-on will be documented in this file.

## [0.1.0] - $(date +%Y-%m-%d)

### Added
- Initial release
- Basic functionality
EOF

# Create .gitignore if needed
cat > "$ADDON_SLUG/.gitignore" << EOF
# Local development
*.log
.DS_Store
__pycache__/
*.pyc
node_modules/
.vscode/
.idea/
EOF

echo ""
echo -e "${GREEN}✅ Add-on created successfully!${NC}"
echo ""
echo -e "${BLUE}📁 Add-on location:${NC} ./${ADDON_SLUG}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. cd ${ADDON_SLUG}/rootfs/app"
echo "  2. Implement your add-on logic"
echo "  3. Test locally: ./.common/build.sh ${ADDON_SLUG} --arch amd64"
echo "  4. Update README.md and DOCS.md with your documentation"
echo "  5. Commit and push - CI/CD will handle the rest!"
echo ""
echo -e "${BLUE}Files created:${NC}"
tree -L 3 "$ADDON_SLUG" 2>/dev/null || find "$ADDON_SLUG" -type f | head -20
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
