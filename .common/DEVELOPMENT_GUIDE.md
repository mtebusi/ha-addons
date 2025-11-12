## 🎓 Development Guide for Casual Publishers

This guide helps you quickly develop and deploy Home Assistant add-ons with confidence, using proven automation as "training wheels."

## 🚀 Quick Start

### Create Your First Add-on (5 minutes)

```bash
# Run the interactive add-on generator
./.common/new-addon.sh

# Answer the prompts:
# - Add-on name: "My Service"
# - Slug: my-service (auto-generated)
# - Description: "My awesome service"
# - Port: 8080
# - Language: Python (or Node.js, Bash)

# Done! Your add-on structure is created
```

### What Just Happened?

The generator created:
- ✅ `config.yaml` - Add-on metadata (name, version, architectures)
- ✅ `Dockerfile` - How to build your container
- ✅ `README.md` - User-facing documentation
- ✅ `rootfs/app/` - Your application code goes here
- ✅ `rootfs/etc/services.d/` - Startup scripts

## 🔄 Development Workflow

### The "Training Wheels" Workflow

Our CI/CD automation handles the hard parts. You just:

1. **Code** - Edit files in `rootfs/app/`
2. **Commit** - Push to GitHub
3. **Relax** - Automation handles:
   - ✅ Building for 5 architectures
   - ✅ Running quality checks
   - ✅ Updating changelogs
   - ✅ Publishing to registry
   - ✅ Updating documentation

### Example Development Session

```bash
# 1. Make changes to your add-on
vim my-addon/rootfs/app/main.py

# 2. Test locally (optional but recommended)
./.common/build.sh my-addon --arch amd64

# 3. Commit your changes
git add my-addon/
git commit -m "feat: add new feature"

# 4. Push - automation takes over!
git push

# 5. GitHub Actions automatically:
#    - Detects you changed "my-addon"
#    - Builds only that add-on (not others)
#    - Publishes to ghcr.io
#    - Updates README
#    - Updates CHANGELOG
```

## 🎮 Commit Message Magic

Control builds with special commit messages:

```bash
# Skip building entirely (for docs-only changes)
git commit -m "docs: update README [skip ci]"

# Build all add-ons (even if only one changed)
git commit -m "fix: update dependencies [build-all]"

# Skip builds with [nobuild]
git commit -m "chore: update comments [nobuild]"
```

## 🏗️ Understanding the Build Process

### What Happens When You Push

```
1. GitHub Actions triggers
   ↓
2. Smart Change Detection
   - Compares your commit to previous
   - Finds which config.yaml files changed
   - Only builds those add-ons (saves time!)
   ↓
3. Pre-build Sanitization
   - Fixes line endings (Windows → Unix)
   - Makes scripts executable
   - Normalizes spacing
   ↓
4. Multi-Architecture Build
   - Builds for: amd64, aarch64, armv7, armhf, i386
   - Uses official Home Assistant builder
   - Caches for faster rebuilds
   ↓
5. Publish to Registry
   - Pushes to ghcr.io/yourusername/
   - Tags with version and "latest"
   ↓
6. Auto-Documentation
   - Updates CHANGELOG.md
   - Regenerates README.md
```

### Why This is Better Than Manual

**Before (manual)**:
- 50+ minutes to build 5 architectures
- Easy to forget steps
- Inconsistent builds
- Manual changelog updates

**After (automated)**:
- 5-10 minutes for single add-on
- Never forget steps - it's automatic
- Consistent, reproducible builds
- Changelogs auto-updated

## 📋 File Structure Explained

### config.yaml - The Heart of Your Add-on

```yaml
name: "My Service"           # Display name
version: "0.1.0"             # Semantic versioning
slug: "my_service"           # Unique ID (no spaces!)
description: "What it does"  # One-liner
url: "https://github.com/..." # Your repo
arch:                        # Which architectures?
  - amd64                    # Intel/AMD 64-bit
  - aarch64                  # ARM 64-bit (Pi 4)
  - armv7                    # ARM 32-bit
startup: services            # or "application"
boot: auto                   # Start on HA boot
hassio_api: true            # Access supervisor
homeassistant_api: true     # Access HA API
ports:
  8080/tcp: 8080            # External:Internal
options:                    # Default config
  log_level: info
schema:                     # Config validation
  log_level: list(debug|info|warning|error)
```

### Dockerfile - Build Instructions

Your Dockerfile is pre-configured! It:
1. Starts from HA base image
2. Installs your dependencies
3. Copies your code from `rootfs/`
4. Sets up metadata

**Most add-ons don't need Dockerfile changes!**

### rootfs/ - Your Application

```
rootfs/
├── app/                    # Your code goes HERE
│   ├── main.py            # Entry point
│   ├── requirements.txt   # Python deps
│   └── ...                # Your modules
└── etc/
    └── services.d/
        └── my-service/
            ├── run         # Startup script
            └── finish      # Cleanup script
```

**Key insight**: Everything in `rootfs/` gets copied to the container's root `/`.
So `rootfs/app/main.py` becomes `/app/main.py` in the container.

## 🧪 Testing Your Add-on

### Local Testing (Recommended)

```bash
# Build for your architecture
./.common/build.sh my-addon --arch amd64

# The build script:
# 1. Reads config.yaml
# 2. Builds Docker image
# 3. Tags appropriately
# 4. Optionally pushes (with --push)
```

### Test in Home Assistant

1. Push your changes to GitHub
2. Wait for build to complete (check Actions tab)
3. In Home Assistant:
   - Add your repository (if not already)
   - Find your add-on
   - Install
   - Check logs for issues

## 🐛 Troubleshooting

### Build Fails

**Check these first:**

1. **Syntax errors in config.yaml**
   ```bash
   # Validate locally
   yamllint my-addon/config.yaml
   ```

2. **Missing dependencies in requirements.txt**
   - Add all Python packages
   - Use specific versions: `flask==3.0.0`

3. **Script not executable**
   - Automation fixes this, but if local build fails:
   ```bash
   chmod +x my-addon/rootfs/etc/services.d/*/run
   ```

4. **Architecture not supported**
   - Some packages don't work on ARM
   - Test on target arch or remove from config.yaml

### Add-on Won't Start

**Check logs in HA:**

1. Supervisor → Add-ons → Your Add-on → Logs

Common issues:
- Port already in use
- Missing config options
- Permission errors
- Dependency conflicts

**Debug mode:**
```yaml
# In config.yaml, temporarily:
options:
  log_level: debug
```

### Architecture-Specific Issues

If builds work on amd64 but fail on ARM:

1. Check if dependencies support ARM
2. Some Python wheels don't exist for ARM
3. Solution: Use Alpine packages instead
   ```dockerfile
   RUN apk add --no-cache py3-numpy
   ```

## 📚 Best Practices for Casual Publishers

### 1. Start Simple

```python
# Good first add-on structure:
def main():
    print("Hello from Home Assistant!")
    while True:
        # Do something useful
        time.sleep(60)
```

Don't overcomplicate! Get something working first.

### 2. Use Semantic Versioning

```
0.1.0 - Initial development
0.2.0 - Added new feature
0.2.1 - Fixed bug
1.0.0 - First stable release
```

Change the version in `config.yaml` when you make changes.

### 3. Let Automation Help You

The workflows are designed to catch issues:
- Linting finds style problems
- Security scans find vulnerabilities
- Multi-arch builds find platform issues

Don't fight the automation - trust it!

### 4. Document as You Go

Update README.md when you add features:
```markdown
## Features
- [x] Basic functionality
- [x] Web UI
- [ ] Advanced settings (TODO)
```

### 5. Version Control Best Practices

```bash
# Good commits (clear, descriptive)
git commit -m "feat: add temperature monitoring"
git commit -m "fix: resolve connection timeout"
git commit -m "docs: update configuration examples"

# Bad commits (vague)
git commit -m "stuff"
git commit -m "fixed it"
git commit -m "update"
```

## 🎯 Common Patterns

### Pattern: Web Service

```python
# main.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from my add-on!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Pattern: Background Worker

```python
# main.py
import time
import logging

logger = logging.getLogger(__name__)

def main():
    while True:
        try:
            # Do work
            logger.info("Processing...")
            time.sleep(60)
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
```

### Pattern: Home Assistant Integration

```python
# Access HA API
import requests
import os

HA_URL = os.getenv('SUPERVISOR_URL', 'http://supervisor/core')
HA_TOKEN = os.getenv('SUPERVISOR_TOKEN', '')

def get_ha_state(entity_id):
    response = requests.get(
        f"{HA_URL}/api/states/{entity_id}",
        headers={'Authorization': f'Bearer {HA_TOKEN}'}
    )
    return response.json()
```

## 🔐 Security Tips

1. **Never commit secrets**
   - Use config options instead
   - Users enter their own API keys

2. **Validate user input**
   ```python
   if not config.get('api_key'):
       raise ValueError("API key required!")
   ```

3. **Use HTTPS when possible**
   - For external API calls
   - For web interfaces

4. **Keep dependencies updated**
   - Automation scans for vulnerabilities weekly
   - Update `requirements.txt` when alerted

## 🎓 Learning Resources

### While You Code

The automation teaches you:
- **Linting failures** → Shows you style improvements
- **Build failures** → Points to actual errors
- **Security scans** → Identifies vulnerabilities

Read the CI/CD logs - they're educational!

### Example: Learning from Lint

```
❌ Lint error: Line too long (120 > 100 characters)
✅ Fix: Break into multiple lines
```

Over time, you'll write better code naturally.

## 🚦 Ready to Ship?

### Pre-Release Checklist

- [ ] Add-on works locally
- [ ] README.md is complete
- [ ] DOCS.md has usage instructions
- [ ] Version bumped in config.yaml
- [ ] CHANGELOG.md updated
- [ ] Committed and pushed
- [ ] CI/CD builds pass (check Actions tab)
- [ ] Tested in real Home Assistant

### Publishing

Just push to `main`! The automation:
1. Builds all architectures
2. Publishes to GitHub Container Registry
3. Users can install from your repository

### Announcing

Share on:
- Home Assistant Community Forum
- r/homeassistant
- Your social media

## 💡 Tips for Success

1. **Start with the generator** - Don't template from scratch
2. **Commit often** - Small changes are easier to debug
3. **Read the logs** - CI/CD tells you exactly what's wrong
4. **Test locally first** - Faster iteration than pushing every time
5. **Ask for help** - GitHub Issues, HA forum, Discord

## 🎉 You're Ready!

You now have:
- ✅ Automated multi-arch builds
- ✅ Quality checks and security scans
- ✅ Auto-generated documentation
- ✅ Changelog automation
- ✅ Quick-start templates

Focus on your add-on logic - let the automation handle the infrastructure!

---

**Questions?** Open an issue or check the [Home Assistant developer docs](https://developers.home-assistant.io/docs/add-ons).
