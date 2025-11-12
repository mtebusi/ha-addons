"""Main ADS-B Dashboard Service."""
import asyncio
import logging
import os
import json
import sys
from pathlib import Path

from scanner import ADSBScanner
from ha_integration import HAIntegration
from tar1090_updater import Tar1090Updater

_LOGGER = logging.getLogger(__name__)


class ADSBService:
    """Main ADS-B Dashboard service."""

    def __init__(self):
        """Initialize service."""
        self.config = self._load_config()
        self.scanner = ADSBScanner(timeout=2)
        self.ha_integration = None
        self.tar1090_updater = Tar1090Updater()
        self.running = False

        # Setup logging
        log_level = self.config.get("log_level", "info").upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout
        )

    def _load_config(self) -> dict:
        """Load add-on configuration."""
        config_path = Path("/data/options.json")
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}

    async def setup(self):
        """Setup service components."""
        _LOGGER.info("Starting ADS-B Dashboard service...")

        # Get supervisor token
        supervisor_token = os.getenv("SUPERVISOR_TOKEN")
        if not supervisor_token:
            _LOGGER.error("SUPERVISOR_TOKEN not found!")
            return False

        # Initialize HA integration
        self.ha_integration = HAIntegration(supervisor_token)
        await self.ha_integration.create_entities()

        # Update tar1090 if enabled
        if self.config.get("update_tar1090", True):
            _LOGGER.info("Updating tar1090...")
            success = await self.tar1090_updater.update()
            if not success:
                _LOGGER.warning("tar1090 update failed, but continuing...")

        # Verify tar1090 is installed
        if not self.tar1090_updater.is_installed():
            _LOGGER.error("tar1090 is not installed!")
            return False

        # Write nginx config with tar1090 location
        self._write_nginx_config()

        _LOGGER.info("Service setup complete")
        return True

    def _write_nginx_config(self):
        """Write nginx configuration for tar1090 and proxy."""
        html_dir = self.tar1090_updater.get_html_dir()

        # Determine device proxy configuration
        proxy_config = ""
        if hasattr(self.scanner, 'detected_device') and self.scanner.detected_device:
            device = self.scanner.detected_device
            proxy_url = f"http://{device['host']}:{device['port']}"

            proxy_config = f"""
        # Proxy to ADS-B device
        location /data/ {{
            proxy_pass {proxy_url}/data/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }}
"""

        nginx_config = f"""
daemon off;
error_log /var/log/nginx/error.log warn;
pid /run/nginx/nginx.pid;

events {{
    worker_connections 1024;
}}

http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;

    sendfile on;
    keepalive_timeout 65;
    gzip on;

    server {{
        listen 8080;
        server_name _;

        root {html_dir};
        index index.html;

        # Serve tar1090 static files
        location / {{
            try_files $uri $uri/ /index.html;
            add_header Cache-Control "public, max-age=3600";
        }}

        # Disable caching for data files
        location ~ \\.(json|geojson)$ {{
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires 0;
        }}
{proxy_config}
        # Health check
        location /health {{
            access_log off;
            return 200 "OK";
            add_header Content-Type text/plain;
        }}
    }}
}}
"""

        config_path = Path("/etc/nginx/nginx.conf")
        config_path.write_text(nginx_config)
        _LOGGER.info("Nginx configuration written")

    async def scan_loop(self):
        """Main scanning loop."""
        scan_interval = self.config.get("scan_interval", 30)
        auto_detect = self.config.get("auto_detect", True)
        manual_host = self.config.get("manual_host", "")
        manual_port = self.config.get("manual_port", 0)

        while self.running:
            try:
                # Scan for device
                if manual_host and manual_port > 0:
                    _LOGGER.info(f"Connecting to manual device: {manual_host}:{manual_port}")
                    device_info = {
                        "host": manual_host,
                        "port": manual_port,
                        "type": "manual",
                        "endpoint": "/data/aircraft.json",
                        "transport": "http"
                    }
                    self.scanner.detected_device = device_info
                elif auto_detect:
                    _LOGGER.info("Scanning network for ADS-B devices...")
                    device_info = await self.scanner.scan_network()
                else:
                    device_info = None

                # Update HA entities
                if device_info:
                    await self.ha_integration.update_receiver_status(True, device_info)

                    # Update nginx config with new device
                    self._write_nginx_config()

                    # Get aircraft data
                    aircraft_data = await self.scanner.get_aircraft_data()
                    await self.ha_integration.update_aircraft_data(aircraft_data)
                else:
                    await self.ha_integration.update_receiver_status(False)
                    await self.ha_integration.update_aircraft_data(None)

            except Exception as e:
                _LOGGER.error(f"Error in scan loop: {e}", exc_info=True)

            # Wait before next scan
            await asyncio.sleep(scan_interval)

    async def update_loop(self):
        """Update aircraft data more frequently."""
        while self.running:
            try:
                if self.scanner.detected_device:
                    aircraft_data = await self.scanner.get_aircraft_data()
                    if aircraft_data:
                        await self.ha_integration.update_aircraft_data(aircraft_data)
            except Exception as e:
                _LOGGER.error(f"Error updating aircraft data: {e}")

            # Update every 5 seconds
            await asyncio.sleep(5)

    async def run(self):
        """Run the service."""
        if not await self.setup():
            _LOGGER.error("Service setup failed")
            return

        self.running = True

        # Start both loops
        try:
            await asyncio.gather(
                self.scan_loop(),
                self.update_loop()
            )
        except asyncio.CancelledError:
            _LOGGER.info("Service cancelled")
        finally:
            self.running = False

    async def stop(self):
        """Stop the service."""
        _LOGGER.info("Stopping service...")
        self.running = False


async def main():
    """Main entry point."""
    service = ADSBService()

    try:
        await service.run()
    except KeyboardInterrupt:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
