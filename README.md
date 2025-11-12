# Home Assistant Add-ons by mtebusi

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

This repository contains Home Assistant add-ons developed by mtebusi. Add-ons extend the functionality of your Home Assistant instance by providing additional services and integrations.

## Available Add-ons

### 🤖 HomeAssistant MCP Server

[![Version][ha-mcp-version-shield]][ha-mcp-readme]
[![Architectures][architectures-shield]][ha-mcp-readme]

MCP (Model Context Protocol) server add-on that enables Claude Desktop to interact with your HomeAssistant instance through its native Connections capability.

**Features:**
- 🔐 Secure OAuth2 Authentication using HomeAssistant's native auth
- 🏠 Locally Hosted - runs directly on your HomeAssistant device
- 🚀 Zero Configuration setup
- 🔧 Comprehensive Control through MCP tools
- 🌍 Multi-Architecture Support (amd64, aarch64, armhf, armv7, i386)

[➡️ Full documentation](ha-mcp-server/README.md)

---

## Installation

### Adding this Repository

1. Open your Home Assistant instance
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the three dots menu (⋮) → **Repositories**
4. Add this repository URL: `https://github.com/mtebusi/ha-addons`
5. Click **Add**

### Installing an Add-on

Once the repository is added:

1. Find the desired add-on in the store
2. Click on the add-on
3. Click **Install**
4. Configure the add-on (if needed)
5. Click **Start**

## Repository Structure

This repository follows a multi-addon structure where each add-on is self-contained:

```
/
├── ha-mcp-server/           # HomeAssistant MCP Server add-on
│   ├── config.yaml         # Add-on configuration
│   ├── Dockerfile          # Container definition
│   ├── README.md           # Add-on documentation
│   └── rootfs/             # Add-on files
│       └── app/            # Application code
├── .common/                 # Shared build scripts and templates
│   ├── build.sh            # Universal build script
│   ├── templates/          # Templates for new add-ons
│   └── README.md           # Development guide
├── .github/                 # CI/CD workflows
│   └── workflows/
│       ├── builder.yml     # Multi-addon build workflow
│       └── lint.yml        # Code quality checks
├── repository.json          # Repository manifest
├── README.md               # This file
└── CLAUDE.md              # AI assistant instructions
```

## Development

### Creating a New Add-on

1. Copy the template:
   ```bash
   cp -r .common/templates/ <new-addon-name>/
   ```

2. Update the configuration files:
   - `config.yaml`: Add-on name, version, slug, description
   - `Dockerfile`: Dependencies and build steps
   - `README.md`: User-facing documentation

3. Implement your add-on functionality in `rootfs/app/`

4. Build locally to test:
   ```bash
   ./.common/build.sh <new-addon-name> --arch amd64
   ```

5. Update this README to list your new add-on

6. Commit and push changes

For detailed development instructions, see [.common/README.md](.common/README.md)

### Building Add-ons

Use the shared build script:

```bash
# Build specific add-on for specific architecture
./.common/build.sh ha-mcp-server --arch amd64

# Build with push to registry
./.common/build.sh ha-mcp-server --arch amd64 --push

# Specify custom registry
./.common/build.sh ha-mcp-server --arch amd64 --registry ghcr.io
```

### CI/CD

This repository uses GitHub Actions for automated building:

- **builder.yml**: Automatically discovers and builds all add-ons for all architectures
- **lint.yml**: Validates Python code, YAML files, Dockerfiles, and add-on configurations
- **test.yml**: Runs automated tests (if present)

Builds are triggered on:
- Push to `main` branch
- Pull requests
- Version tags (`v*`)

## Architecture Support

All add-ons support multiple architectures:

| Architecture | Description |
|--------------|-------------|
| amd64 | 64-bit x86 (Intel/AMD) |
| aarch64 | 64-bit ARM (Raspberry Pi 4, etc.) |
| armhf | 32-bit ARM with hardware floating point |
| armv7 | 32-bit ARMv7 |
| i386 | 32-bit x86 |

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes
4. Add tests if applicable
5. Ensure all CI checks pass
6. Submit a pull request

### Pull Request Guidelines

- Follow existing code style and conventions
- Update documentation as needed
- Add changelog entries for user-facing changes
- Test on multiple architectures when possible
- Keep commits focused and well-described

## Support

- **Issues**: [GitHub Issues](https://github.com/mtebusi/ha-addons/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mtebusi/ha-addons/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## License

All add-ons in this repository are licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Home Assistant community for the amazing platform
- All contributors and testers
- Open source projects that make this possible

---

[releases-shield]: https://img.shields.io/github/release/mtebusi/ha-addons.svg
[releases]: https://github.com/mtebusi/ha-addons/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/mtebusi/ha-addons.svg
[commits]: https://github.com/mtebusi/ha-addons/commits/main
[license-shield]: https://img.shields.io/github/license/mtebusi/ha-addons.svg
[ha-mcp-version-shield]: https://img.shields.io/badge/version-0.0.1-blue.svg
[ha-mcp-readme]: ha-mcp-server/README.md
[architectures-shield]: https://img.shields.io/badge/architectures-amd64%20%7C%20aarch64%20%7C%20armhf%20%7C%20armv7%20%7C%20i386-green.svg
