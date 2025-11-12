# Shared Resources for Home Assistant Add-ons

This directory contains shared scripts and templates used across all add-ons in this repository.

## Contents

### Build Scripts

- **build.sh**: Universal build script for building add-on Docker images
  - Usage: `./.common/build.sh <addon-dir> [--arch <arch>] [--push]`
  - Example: `./.common/build.sh ha-mcp-server --arch amd64`

### Templates

The `templates/` directory contains starter templates for creating new add-ons:

- `config.yaml.template`: Basic add-on configuration
- `Dockerfile.template`: Standard Dockerfile structure
- `README.md.template`: Add-on documentation template
- `DOCS.md.template`: User-facing documentation template

## Adding a New Add-on

1. Copy the templates directory: `cp -r .common/templates/ <new-addon-name>/`
2. Update the configuration files with your add-on details
3. Implement your add-on functionality in `rootfs/app/`
4. Update `repository.json` to include your new add-on
5. Build locally: `./.common/build.sh <new-addon-name> --arch amd64`
6. Test the add-on in your Home Assistant instance
7. Commit and push changes

## Architecture Support

All add-ons should support multiple architectures:
- amd64 (64-bit x86)
- aarch64 (64-bit ARM)
- armhf (32-bit ARM with hardware floating point)
- armv7 (32-bit ARMv7)
- i386 (32-bit x86)

Use the base images from Home Assistant:
- `ghcr.io/home-assistant/<arch>-base:latest`
- `ghcr.io/home-assistant/<arch>-base-python:3.12` (for Python add-ons)

## Best Practices

1. **Security**: Always use AppArmor profiles and follow least-privilege principles
2. **Documentation**: Keep DOCS.md updated for users and README.md for developers
3. **Versioning**: Follow semantic versioning (MAJOR.MINOR.PATCH)
4. **Changelog**: Update CHANGELOG.md with each release
5. **Testing**: Test on multiple architectures before releasing
6. **Dependencies**: Keep dependencies minimal and up-to-date
7. **Logs**: Use structured logging with appropriate log levels
