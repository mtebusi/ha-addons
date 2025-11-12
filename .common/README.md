# Shared Resources for Home Assistant Add-ons

This directory contains shared scripts, templates, and automation for managing multiple Home Assistant add-ons.

## 🚀 Quick Start (New to add-on development?)

**The easiest way to create a new add-on:**

```bash
./.common/new-addon.sh
```

This interactive script will:
- ✅ Ask you a few simple questions
- ✅ Generate a complete add-on structure
- ✅ Set up proper Docker configuration
- ✅ Create starter code (Python/Node.js/Bash)
- ✅ Configure CI/CD integration

**Then read**: [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for step-by-step instructions.

## 📁 Contents

### Scripts

- **new-addon.sh**: Interactive add-on generator (⭐ Start here!)
- **build.sh**: Universal build script for local testing
  - Usage: `./.common/build.sh <addon-dir> [--arch <arch>] [--push]`
  - Example: `./.common/build.sh ha-mcp-server --arch amd64`

### Templates

The `templates/` directory contains starter files:

- `config.yaml.template`: Basic add-on configuration
- `Dockerfile.template`: Standard Dockerfile structure
- `README.md.template`: Add-on documentation template

**Note**: Use `new-addon.sh` instead of copying templates manually!

### Documentation

- **DEVELOPMENT_GUIDE.md**: Comprehensive guide for casual publishers
  - Quick start tutorial
  - Best practices
  - Troubleshooting
  - Common patterns
  - Security tips

## 🎯 Recommended Workflow

### For First-Time Publishers

1. **Create**: Run `./.common/new-addon.sh`
2. **Learn**: Read [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
3. **Code**: Edit files in `<addon>/rootfs/app/`
4. **Test**: `./.common/build.sh <addon> --arch amd64`
5. **Push**: Automation handles the rest!

### For Experienced Developers

1. Create add-on structure (manually or via script)
2. Implement logic in `rootfs/app/`
3. Test locally with build.sh
4. Commit - CI/CD builds all architectures
5. Publish automatically to ghcr.io

## 🤖 Automation Features

This repository includes powerful automation:

### Smart Build System
- **Change Detection**: Only builds add-ons that changed
- **Multi-Architecture**: Automatic builds for 5 architectures
- **Pre-build Sanitization**: Fixes common issues automatically
- **Caching**: Fast rebuilds using GitHub Actions cache

### Quality Assurance
- **Linting**: Python, YAML, Dockerfile validation
- **Security Scanning**: Weekly vulnerability checks
- **Config Validation**: Ensures all add-ons are properly configured

### Documentation
- **Auto-README**: Daily updates to repository README
- **Changelog**: Automatic changelog updates on version changes
- **Version Tracking**: Automated version management

### Commit Message Controls

```bash
# Skip building (docs-only changes)
git commit -m "docs: update README [skip ci]"

# Build all add-ons (even if only one changed)
git commit -m "fix: dependencies [build-all]"

# Skip with alternative syntax
git commit -m "chore: cleanup [nobuild]"
```

## 🏗️ Architecture Support

All add-ons should support multiple architectures:

| Architecture | Description | Common Devices |
|--------------|-------------|----------------|
| amd64 | 64-bit x86 | Most PCs, servers |
| aarch64 | 64-bit ARM | Raspberry Pi 4, newer SBCs |
| armv7 | 32-bit ARMv7 | Raspberry Pi 2/3 |
| armhf | 32-bit ARM w/ FPU | Older ARM devices |
| i386 | 32-bit x86 | Legacy PCs |

### Base Images

Use official Home Assistant images:

```dockerfile
# For basic add-ons
FROM ghcr.io/home-assistant/<arch>-base:latest

# For Python add-ons
FROM ghcr.io/home-assistant/<arch>-base-python:3.12

# For Node.js add-ons
FROM ghcr.io/home-assistant/<arch>-base-nodejs:18
```

## 📚 Best Practices

### Security
1. Always use AppArmor profiles
2. Never commit secrets (use config options)
3. Validate all user inputs
4. Keep dependencies updated
5. Use HTTPS when possible

### Code Quality
1. Follow semantic versioning (MAJOR.MINOR.PATCH)
2. Update CHANGELOG.md with each release
3. Write clear commit messages
4. Test on multiple architectures
5. Document configuration options

### Development Speed
1. Use the add-on generator for new projects
2. Test locally before pushing
3. Let automation handle builds
4. Trust the quality checks
5. Read CI/CD logs to learn

## 🐛 Troubleshooting

### Build Failures

**"config.yaml not found"**
- Ensure your add-on directory has config.yaml
- Check file name spelling

**"Architecture not supported"**
- Some packages don't work on ARM
- Remove unsupported archs from config.yaml

**"Permission denied"**
- Scripts in `rootfs/etc/services.d/` must be executable
- Automation fixes this, but check locally

### Local Testing Issues

**"Docker build fails"**
- Check Dockerfile syntax
- Verify dependencies exist for base image
- Test with: `docker build -t test .`

**"Add-on won't start"**
- Check logs in Home Assistant
- Set `log_level: debug` in config
- Verify service scripts are correct

## 💡 Tips for Success

1. **Start Simple**: Get basic functionality working first
2. **Use Automation**: Let CI/CD be your safety net
3. **Read Logs**: They tell you exactly what's wrong
4. **Ask for Help**: GitHub Issues, HA forums
5. **Iterate Quickly**: Small commits, frequent pushes

## 📖 Learning Resources

- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)**: Comprehensive tutorial
- **[Home Assistant Add-on Docs](https://developers.home-assistant.io/docs/add-ons)**: Official documentation
- **[Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)**: Container optimization
- **Existing Add-ons**: Look at ha-mcp-server for examples

## 🎉 Ready to Build?

```bash
# Create your first add-on
./.common/new-addon.sh

# Then read the development guide
cat .common/DEVELOPMENT_GUIDE.md
```

Happy coding! 🚀
