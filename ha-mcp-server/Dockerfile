ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/sh", "-c"]

# Setup base system and Python 3.12
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        nginx \
        openssl

# Copy root filesystem (includes app code in /app)
COPY rootfs /

# Install Python dependencies
RUN \
    python3 -m pip install --no-cache-dir --break-system-packages -r /app/requirements.txt \
    && rm -f /app/requirements.txt

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
    org.opencontainers.image.vendor="HomeAssistant MCP Server" \
    org.opencontainers.image.authors="mtebusi <mtebusi@example.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/mtebusi/ha-mcp-v2" \
    org.opencontainers.image.source="https://github.com/mtebusi/ha-mcp-v2" \
    org.opencontainers.image.documentation="https://github.com/mtebusi/ha-mcp-v2/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}