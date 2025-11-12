ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/sh", "-c"]

# Install dependencies
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        nginx \
        git \
        curl \
        && rm -rf /var/cache/apk/*

# Copy root filesystem
COPY rootfs /

# Install Python dependencies
RUN \
    python3 -m pip install --no-cache-dir --break-system-packages -r /app/requirements.txt \
    && rm -f /app/requirements.txt

# Create nginx directories and set permissions
RUN \
    mkdir -p /var/www/tar1090 \
    && mkdir -p /run/nginx \
    && mkdir -p /var/log/nginx \
    && chown -R nginx:nginx /var/www/tar1090 \
    && chown -R nginx:nginx /run/nginx \
    && chown -R nginx:nginx /var/log/nginx

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
    maintainer="mtebusi" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="HomeAssistant ADS-B Dashboard" \
    org.opencontainers.image.authors="mtebusi" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/mtebusi/ha-addons" \
    org.opencontainers.image.source="https://github.com/mtebusi/ha-addons" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
