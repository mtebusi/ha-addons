"""ADS-B Network Scanner - Discovers ADS-B receivers on local network."""
import asyncio
import logging
import socket
import aiohttp
from typing import Optional, Dict, List, Tuple

_LOGGER = logging.getLogger(__name__)

# Common ADS-B ports and endpoints
ADSB_PORTS = [30002, 30003, 30005, 30104, 8080, 8081, 80]
ADSB_HTTP_PATHS = [
    "/data/aircraft.json",
    "/tar1090/data/aircraft.json",
    "/skyaware/data/aircraft.json",
    "/dump1090/data/aircraft.json",
]


class ADSBScanner:
    """Scanner for ADS-B receivers on local network."""

    def __init__(self, timeout: int = 2):
        """Initialize scanner."""
        self.timeout = timeout
        self.detected_device: Optional[Dict] = None

    async def scan_network(self, specific_host: Optional[str] = None) -> Optional[Dict]:
        """
        Scan local network for ADS-B devices.

        Args:
            specific_host: If provided, only scan this specific host

        Returns:
            Dict with device info if found, None otherwise
        """
        if specific_host:
            hosts = [specific_host]
        else:
            hosts = await self._get_local_subnet_hosts()

        _LOGGER.info(f"Scanning {len(hosts)} hosts for ADS-B receivers...")

        tasks = [self._scan_host(host) for host in hosts]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if result and not isinstance(result, Exception):
                self.detected_device = result
                _LOGGER.info(f"Found ADS-B device: {result}")
                return result

        _LOGGER.warning("No ADS-B devices found on network")
        return None

    async def _get_local_subnet_hosts(self) -> List[str]:
        """Get list of hosts in local subnet to scan."""
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # Generate subnet IPs (simple /24 subnet)
            base_ip = ".".join(local_ip.split(".")[:-1])
            hosts = [f"{base_ip}.{i}" for i in range(1, 255)]

            _LOGGER.debug(f"Local IP: {local_ip}, scanning subnet {base_ip}.0/24")
            return hosts
        except Exception as e:
            _LOGGER.error(f"Failed to determine local subnet: {e}")
            return []

    async def _scan_host(self, host: str) -> Optional[Dict]:
        """Scan a single host for ADS-B services."""
        for port in ADSB_PORTS:
            # Try HTTP endpoints
            if port in [8080, 8081, 80]:
                device_info = await self._check_http_endpoint(host, port)
                if device_info:
                    return device_info

            # Try TCP connection for raw data ports
            else:
                if await self._check_tcp_port(host, port):
                    # If TCP port is open, try to verify it's ADS-B
                    device_info = await self._identify_adsb_device(host, port)
                    if device_info:
                        return device_info

        return None

    async def _check_tcp_port(self, host: str, port: int) -> bool:
        """Check if TCP port is open."""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False

    async def _check_http_endpoint(self, host: str, port: int) -> Optional[Dict]:
        """Check HTTP endpoints for ADS-B data."""
        for path in ADSB_HTTP_PATHS:
            try:
                url = f"http://{host}:{port}{path}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                        if response.status == 200:
                            data = await response.json()
                            if "aircraft" in data or "now" in data:
                                device_type = self._identify_device_type(path, data)
                                return {
                                    "host": host,
                                    "port": port,
                                    "type": device_type,
                                    "endpoint": path,
                                    "transport": "http"
                                }
            except (asyncio.TimeoutError, aiohttp.ClientError, Exception):
                continue

        return None

    async def _identify_adsb_device(self, host: str, port: int) -> Optional[Dict]:
        """Identify ADS-B device by checking common HTTP ports."""
        # If raw data port is open, check for web interface on port 8080
        http_ports = [8080, 8081, 80]
        for http_port in http_ports:
            device_info = await self._check_http_endpoint(host, http_port)
            if device_info:
                device_info["raw_port"] = port
                return device_info

        # If no HTTP interface found, assume it's a raw feed
        return {
            "host": host,
            "port": port,
            "type": "dump1090",
            "endpoint": None,
            "transport": "tcp"
        }

    def _identify_device_type(self, path: str, data: Dict) -> str:
        """Identify device type from path and data."""
        if "tar1090" in path:
            return "tar1090"
        elif "skyaware" in path:
            return "piaware"
        elif "dump1090" in path:
            return "dump1090"
        elif data.get("version"):
            return data.get("version", "unknown")
        else:
            return "readsb"

    async def get_aircraft_data(self) -> Optional[Dict]:
        """Get current aircraft data from detected device."""
        if not self.detected_device:
            return None

        device = self.detected_device

        if device["transport"] == "http":
            try:
                url = f"http://{device['host']}:{device['port']}{device['endpoint']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                        if response.status == 200:
                            return await response.json()
            except Exception as e:
                _LOGGER.error(f"Failed to get aircraft data: {e}")
                return None

        return None

    def get_device_info(self) -> Optional[Dict]:
        """Get detected device information."""
        return self.detected_device
