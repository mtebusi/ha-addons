# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Home Assistant Add-ons Repository** - A multi-addon repository containing Home Assistant add-ons that extend the functionality of Home Assistant instances. This repository follows the pattern of hosting multiple add-ons in a single repository with shared build infrastructure.

### Repository Structure

This repository uses a **flat multi-addon architecture** where:
- Each add-on is self-contained in its own root-level directory
- Shared build scripts and templates are in `.common/`
- CI/CD automatically discovers and builds all add-ons
- Each add-on can be developed and released independently

### Current Add-ons

1. **ha-mcp-server**: MCP (Model Context Protocol) server that enables Claude Desktop to interact with HomeAssistant instances through OAuth2 authentication and SSE-based connections

## Directory Structure

```
/
├── ha-mcp-server/              # MCP Server Add-on
│   ├── config.yaml            # Add-on configuration manifest
│   ├── Dockerfile             # Multi-stage, multi-arch Dockerfile
│   ├── build.yaml             # Build configuration for architectures
│   ├── apparmor.txt          # AppArmor security profile
│   ├── CHANGELOG.md          # Version changelog
│   ├── DOCS.md               # User documentation
│   ├── README.md             # Add-on description
│   └── rootfs/               # Add-on runtime files
│       ├── etc/              # Service configuration
│       │   └── services.d/   # s6-overlay services
│       └── app/              # Application code
│           ├── __init__.py
│           ├── server.py     # Main MCP server
│           ├── auth.py       # OAuth2 authentication
│           ├── config.py     # Configuration management
│           ├── constants.py  # Version and constants
│           ├── requirements.txt  # Python dependencies
│           ├── tools/        # MCP tools implementation
│           ├── ha_api/       # HomeAssistant API clients
│           └── mcp/          # MCP protocol implementation
├── .common/                   # Shared resources
│   ├── build.sh              # Universal build script
│   ├── templates/            # Templates for new add-ons
│   │   ├── config.yaml.template
│   │   ├── Dockerfile.template
│   │   └── README.md.template
│   └── README.md             # Development guide
├── .github/                   # GitHub configuration
│   └── workflows/
│       ├── builder.yml       # Multi-addon build workflow
│       └── lint.yml          # Code quality checks
├── scripts/                   # Legacy build scripts
├── repository.json            # Add-on repository manifest
├── README.md                 # Repository documentation
├── CLAUDE.md                 # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore configuration
```

## Version Management

Each add-on manages its own version independently in its `config.yaml` file:

```yaml
# ha-mcp-server/config.yaml
version: "0.0.1"
```

Update the version in the add-on's `config.yaml` when making changes.

## Development Commands

### Building Add-ons

```bash
# Build specific add-on for specific architecture
./.common/build.sh <addon-dir> --arch amd64

# Build with push to registry
./.common/build.sh <addon-dir> --arch amd64 --push

# Examples
./.common/build.sh ha-mcp-server --arch amd64
./.common/build.sh ha-mcp-server --arch aarch64 --push
```

### Linting and Validation

```bash
# Python linting (if add-on has Python code)
find <addon-dir>/rootfs/app -name "*.py" -exec ruff check {} +
find <addon-dir>/rootfs/app -name "*.py" -exec black --check {} +

# YAML validation
yamllint <addon-dir>/config.yaml

# Dockerfile linting
hadolint <addon-dir>/Dockerfile

# Validate add-on configuration
python -c "
import yaml
with open('<addon-dir>/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    required = ['name', 'version', 'slug', 'description', 'arch']
    for field in required:
        assert field in config, f'Missing {field}'
"
```

### Testing

Tests should be placed in the add-on directory:

```bash
# Run add-on specific tests
pytest <addon-dir>/tests/ -v

# For ha-mcp-server
pytest ha-mcp-server/tests/ -v
```

## Creating a New Add-on

### Step-by-Step Guide

1. **Copy the template**:
   ```bash
   cp -r .common/templates/ <new-addon-name>/
   ```

2. **Configure the add-on** (`<new-addon-name>/config.yaml`):
   ```yaml
   name: "Your Add-on Name"
   version: "0.1.0"
   slug: "your_addon_slug"
   description: "Brief description"
   url: "https://github.com/mtebusi/ha-addons"
   arch:
     - amd64
     - aarch64
     - armhf
     - armv7
     - i386
   startup: services
   boot: auto
   # ... other configuration
   image: "ghcr.io/mtebusi/{arch}-your-addon-slug"
   ```

3. **Create the directory structure**:
   ```bash
   mkdir -p <new-addon-name>/rootfs/app
   mkdir -p <new-addon-name>/rootfs/etc/services.d/<service-name>
   ```

4. **Implement the Dockerfile**:
   - Use the template as a starting point
   - Install dependencies
   - Copy rootfs directory
   - Set working directory to `/app`

5. **Implement the application** in `rootfs/app/`:
   - Add your application code
   - Create `requirements.txt` if using Python
   - Implement service startup scripts in `rootfs/etc/services.d/`

6. **Create service scripts** (if needed):

   `rootfs/etc/services.d/<service-name>/run`:
   ```bash
   #!/usr/bin/with-contenv bashio
   bashio::log.info "Starting service..."
   cd /app
   exec python -m your_module
   ```

   `rootfs/etc/services.d/<service-name>/finish`:
   ```bash
   #!/usr/bin/execlineb -S0
   if { s6-test ${1} -ne 0 }
   if { s6-test ${1} -ne 256 }
   s6-svscanctl -t /var/run/s6/services
   ```

7. **Write documentation**:
   - Update `README.md` with add-on details
   - Update `DOCS.md` with user instructions
   - Create `CHANGELOG.md`

8. **Test locally**:
   ```bash
   ./.common/build.sh <new-addon-name> --arch amd64
   ```

9. **Update repository README**:
   - Add your add-on to the list in `/README.md`

10. **Commit and push**:
    ```bash
    git add <new-addon-name>/
    git add README.md
    git commit -m "feat: add <new-addon-name> add-on"
    git push
    ```

## GitHub Workflows

### Multi-Addon Builder (`builder.yml`)

The builder workflow automatically:
1. Discovers all add-ons (directories with `config.yaml`)
2. Builds each add-on for all architectures
3. Pushes images to GitHub Container Registry
4. Uses build caching for faster builds

The workflow triggers on:
- Push to `main` branch
- Pull requests
- Version tags (`v*`)
- Manual workflow dispatch

### Lint and Validate (`lint.yml`)

The lint workflow:
1. Finds and lints all Python code in `*/rootfs/app/`
2. Validates all YAML files
3. Lints all Dockerfiles
4. Validates add-on configurations
5. Runs security scanning

## Add-on Configuration Schema

### Required Fields

```yaml
name: "string"          # Display name
version: "x.y.z"        # Semantic version
slug: "addon_slug"      # Unique identifier (lowercase, underscores)
description: "string"   # Brief description
arch:                   # Supported architectures (array)
  - amd64
  - aarch64
  - armhf
  - armv7
  - i386
```

### Common Optional Fields

```yaml
url: "https://..."              # Project URL
startup: services|application   # Startup type
boot: auto|manual              # Auto-start on boot
init: true|false               # Use s6-overlay init
hassio_api: true|false         # Access to Supervisor API
homeassistant_api: true|false  # Access to HA API
auth_api: true|false           # Access to Auth API
ingress: true|false            # Enable Ingress
ingress_port: 8080             # Ingress port
panel_icon: mdi:icon           # Panel icon
panel_title: "Title"           # Panel title
ports:                         # Port mappings
  8080/tcp: 8080
options:                       # Default configuration
  log_level: info
schema:                        # Configuration schema
  log_level: list(debug|info|warning|error)
image: "registry/image"        # Docker image template
apparmor: true|false          # Enable AppArmor
```

## Docker Image Naming

Images follow this naming convention:
```
ghcr.io/{owner}/{arch}-{slug}:{version}
ghcr.io/{owner}/{arch}-{slug}:latest
```

Example:
```
ghcr.io/mtebusi/amd64-ha_mcp_server:0.0.1
ghcr.io/mtebusi/amd64-ha_mcp_server:latest
```

## Architecture Support

All add-ons should support multiple architectures using multi-arch Docker builds:

| Architecture | Base Image |
|--------------|------------|
| amd64 | ghcr.io/home-assistant/amd64-base:latest |
| aarch64 | ghcr.io/home-assistant/aarch64-base:latest |
| armhf | ghcr.io/home-assistant/armhf-base:latest |
| armv7 | ghcr.io/home-assistant/armv7-base:latest |
| i386 | ghcr.io/home-assistant/i386-base:latest |

For Python add-ons, use:
```
ghcr.io/home-assistant/{arch}-base-python:3.12
```

## Best Practices

### Security

1. Use AppArmor profiles for all add-ons
2. Follow principle of least privilege
3. Never store secrets in code
4. Use Home Assistant's built-in authentication
5. Validate all user inputs
6. Keep dependencies up-to-date

### Code Organization

1. Keep add-on code in `rootfs/app/`
2. Use `rootfs/etc/services.d/` for service management
3. Configuration files go in `rootfs/etc/` or `/data/`
4. Use `/config/` for Home Assistant configuration access
5. Store persistent data in `/data/`

### Documentation

1. Keep README.md updated with features and installation
2. DOCS.md should have user-facing configuration docs
3. Update CHANGELOG.md with each version
4. Include examples in documentation
5. Document all configuration options

### Versioning

1. Follow semantic versioning (MAJOR.MINOR.PATCH)
2. Update version in `config.yaml` for each release
3. Tag releases with `v` prefix: `v1.0.0`
4. Update CHANGELOG.md before releasing
5. Test on multiple architectures before releasing

### CI/CD

1. All add-ons are built automatically on push
2. Pull requests run linting and validation
3. Builds are cached for faster iteration
4. Images are pushed to GitHub Container Registry
5. Failed builds block merging

## Troubleshooting

### Build Issues

1. **Dockerfile errors**: Check base image compatibility
2. **Missing dependencies**: Update package lists in Dockerfile
3. **Architecture-specific issues**: Test on target architecture
4. **Build timeouts**: Optimize build steps, use caching

### Runtime Issues

1. **Add-on won't start**: Check logs in Home Assistant
2. **Permission errors**: Review AppArmor profile
3. **API access issues**: Verify `*_api` flags in config.yaml
4. **Service crashes**: Check service scripts in `services.d/`

### Common Gotchas

1. **Paths**: Use absolute paths in scripts
2. **Dependencies**: Install all dependencies in Dockerfile
3. **Logs**: Use bashio logging helpers for proper log levels
4. **Configuration**: Validate user config before using
5. **Networking**: Use Home Assistant Ingress when possible

## Quick Reference

### Key Files to Edit

For existing add-ons:
- `<addon>/config.yaml` - Add-on configuration
- `<addon>/Dockerfile` - Container definition
- `<addon>/rootfs/app/` - Application code
- `<addon>/README.md` - Add-on documentation
- `<addon>/CHANGELOG.md` - Version history

For repository:
- `README.md` - Repository documentation
- `.github/workflows/builder.yml` - Build automation
- `.common/build.sh` - Build script

### Testing Checklist

Before committing:
- [ ] Add-on builds successfully locally
- [ ] Configuration validates correctly
- [ ] All required files present (README, Dockerfile, config.yaml)
- [ ] CHANGELOG updated
- [ ] Version bumped if needed
- [ ] Documentation updated
- [ ] Tested on local Home Assistant (if possible)
- [ ] Linting passes
- [ ] No secrets committed

## Important Notes

1. **Multi-addon architecture**: Each add-on is independent with its own versioning
2. **Shared infrastructure**: Use `.common/` for shared scripts and templates
3. **Automatic discovery**: CI/CD automatically finds and builds all add-ons
4. **Independent releases**: Add-ons can be released independently
5. **No breaking changes**: Maintain backwards compatibility when possible
6. **Documentation first**: Update docs before or with code changes
7. **Security focus**: Always consider security implications
8. **Test thoroughly**: Test on multiple architectures
9. **Follow conventions**: Maintain consistency across add-ons
10. **Keep it simple**: Minimize dependencies and complexity
