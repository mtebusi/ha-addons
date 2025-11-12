"""tar1090 Updater - Downloads and updates tar1090 from GitHub."""
import logging
import os
import subprocess
import shutil
from pathlib import Path

_LOGGER = logging.getLogger(__name__)

TAR1090_REPO = "https://github.com/wiedehopf/tar1090.git"
TAR1090_DIR = "/var/www/tar1090"
TAR1090_HTML_DIR = "/var/www/tar1090/html"


class Tar1090Updater:
    """Manages tar1090 installation and updates."""

    def __init__(self, install_dir: str = TAR1090_DIR):
        """Initialize updater."""
        self.install_dir = Path(install_dir)
        self.html_dir = self.install_dir / "html"

    async def update(self) -> bool:
        """Download or update tar1090 from GitHub."""
        try:
            _LOGGER.info("Updating tar1090 from GitHub...")

            # Create install directory if it doesn't exist
            self.install_dir.mkdir(parents=True, exist_ok=True)

            # Check if git repo already exists
            if (self.install_dir / ".git").exists():
                _LOGGER.info("Updating existing tar1090 installation...")
                result = subprocess.run(
                    ["git", "-C", str(self.install_dir), "pull"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                _LOGGER.info("Cloning tar1090 from GitHub...")
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", TAR1090_REPO, str(self.install_dir)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

            if result.returncode != 0:
                _LOGGER.error(f"Git operation failed: {result.stderr}")
                return False

            _LOGGER.info("tar1090 updated successfully")

            # Verify HTML directory exists
            if not self.html_dir.exists():
                _LOGGER.error(f"HTML directory not found: {self.html_dir}")
                return False

            # Set proper permissions
            subprocess.run(
                ["chown", "-R", "nginx:nginx", str(self.install_dir)],
                timeout=10
            )

            return True

        except subprocess.TimeoutExpired:
            _LOGGER.error("tar1090 update timed out")
            return False
        except Exception as e:
            _LOGGER.error(f"Failed to update tar1090: {e}")
            return False

    def get_html_dir(self) -> str:
        """Get the path to tar1090 HTML directory."""
        return str(self.html_dir)

    def is_installed(self) -> bool:
        """Check if tar1090 is installed."""
        return self.html_dir.exists() and (self.html_dir / "index.html").exists()
