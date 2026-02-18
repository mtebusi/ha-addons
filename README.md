# Home Assistant Add-ons by mtebusi

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

This repository contains Home Assistant add-ons developed by mtebusi. Add-ons extend the functionality of your Home Assistant instance by providing additional services and integrations.

**Current add-ons:** 2 | **Last updated:** 2026-02-18

## 📦 Available Add-ons

| Add-on | Version | Description | Architectures |
|--------|---------|-------------|---------------|
| [ADS-B Dashboard](ha-adsb/README.md) | `0.1.0` | Lightweight ADS-B receiver dashboard with auto-discovery and tar1090 integration | `amd64` `aarch64` `armv7` `armhf` `i386` |
| [HomeAssistant MCP Server](ha-mcp-server/README.md) | `0.0.1` | MCP server for Claude Desktop integration with HomeAssistant | `amd64` `aarch64` `armv7` `armhf` `i386` |

---

## 🚀 Installation

### Adding this Repository

1. Open your Home Assistant instance
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the three dots menu (⋮) → **Repositories**
4. Add this repository URL: `https://github.com/mtebusi/ha-addons`
5. Click **Add**

[![Open your Home Assistant instance and show the add add-on repository dialog with this repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmtebusi%2Fha-addons)

### Installing an Add-on

Once the repository is added:

1. Find the desired add-on in the store
2. Click on the add-on
3. Click **Install**
4. Configure the add-on (if needed)
5. Click **Start**

## 🛠️ Development

This repository uses a multi-addon architecture with shared infrastructure.

### Quick Start - Creating a New Add-on

```bash
# 1. Copy the template
cp -r .common/templates/ my-new-addon/

# 2. Update configuration
vim my-new-addon/config.yaml

# 3. Implement your add-on
mkdir -p my-new-addon/rootfs/app
# Add your code here

# 4. Test locally
./.common/build.sh my-new-addon --arch amd64

# 5. Commit - CI/CD handles the rest!
git add my-new-addon/
git commit -m "feat: add my-new-addon"
git push
```

### Repository Structure

```
/
├── <addon-name>/           # Each add-on in its own directory
│   ├── config.yaml        # Add-on configuration
│   ├── Dockerfile         # Container definition
│   ├── README.md          # Add-on documentation
│   └── rootfs/            # Add-on runtime files
│       └── app/           # Application code
├── .common/                # Shared resources
│   ├── build.sh           # Universal build script
│   └── templates/         # Templates for new add-ons
└── .github/workflows/      # Automated CI/CD
```

### Automation Features

This repository includes several automated workflows:

- 🏗️ **Smart Builds**: Only builds add-ons that changed
- 📝 **Auto-Changelog**: Automatically updates CHANGELOG.md
- 📋 **README Updates**: This file is auto-generated daily
- ✅ **Quality Checks**: Linting and validation on every commit
- 🔒 **Security Scans**: Weekly security vulnerability scanning

### Build Control

Control builds with commit messages:

- `[skip ci]` or `[nobuild]` - Skip building entirely
- `[build-all]` - Force build all add-ons

For detailed development instructions, see [.common/README.md](.common/README.md)

## 🏗️ Architecture Support

All add-ons support multiple architectures:

| Architecture | Description |
|--------------|-------------|
| amd64 | 64-bit x86 (Intel/AMD) |
| aarch64 | 64-bit ARM (Raspberry Pi 4, etc.) |
| armhf | 32-bit ARM with hardware floating point |
| armv7 | 32-bit ARMv7 |
| i386 | 32-bit x86 |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes
4. Let CI/CD validate your changes
5. Submit a pull request

The automated workflows will handle building, testing, and validation.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/mtebusi/ha-addons/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mtebusi/ha-addons/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## 📜 License

All add-ons in this repository are licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Home Assistant community for the amazing platform
- All contributors and testers
- Inspiration from [alexbelgium/hassio-addons](https://github.com/alexbelgium/hassio-addons) and [dianlight/hassio-addons](https://github.com/dianlight/hassio-addons)

---

[releases-shield]: https://img.shields.io/github/release/mtebusi/ha-addons.svg
[releases]: https://github.com/mtebusi/ha-addons/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/mtebusi/ha-addons.svg
[commits]: https://github.com/mtebusi/ha-addons/commits/main
[license-shield]: https://img.shields.io/github/license/mtebusi/ha-addons.svg
