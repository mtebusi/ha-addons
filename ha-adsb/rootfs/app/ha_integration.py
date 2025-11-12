"""HomeAssistant Integration - Manages entities for ADS-B data."""
import logging
import asyncio
import aiohttp
from typing import Optional, Dict, Any

_LOGGER = logging.getLogger(__name__)


class HAIntegration:
    """HomeAssistant API integration for ADS-B entities."""

    def __init__(self, supervisor_token: str, ha_url: str = "http://supervisor/core"):
        """Initialize HA integration."""
        self.supervisor_token = supervisor_token
        self.ha_url = ha_url
        self.headers = {
            "Authorization": f"Bearer {supervisor_token}",
            "Content-Type": "application/json",
        }
        self.entities_created = False

    async def create_entities(self):
        """Create/register entities in HomeAssistant."""
        if self.entities_created:
            return

        entities = [
            {
                "entity_id": "binary_sensor.adsb_receiver",
                "state": "off",
                "attributes": {
                    "friendly_name": "ADS-B Receiver Status",
                    "device_class": "connectivity",
                    "icon": "mdi:airplane",
                }
            },
            {
                "entity_id": "sensor.adsb_aircraft_count",
                "state": "0",
                "attributes": {
                    "friendly_name": "Visible Aircraft",
                    "unit_of_measurement": "aircraft",
                    "icon": "mdi:airplane-clock",
                }
            },
            {
                "entity_id": "sensor.adsb_message_rate",
                "state": "0",
                "attributes": {
                    "friendly_name": "Message Rate",
                    "unit_of_measurement": "msg/s",
                    "icon": "mdi:radio-tower",
                }
            },
            {
                "entity_id": "sensor.adsb_receiver_type",
                "state": "unknown",
                "attributes": {
                    "friendly_name": "Receiver Type",
                    "icon": "mdi:chip",
                }
            },
            {
                "entity_id": "sensor.adsb_receiver_location",
                "state": "unknown",
                "attributes": {
                    "friendly_name": "Receiver Location",
                    "icon": "mdi:map-marker-radius",
                }
            },
        ]

        for entity in entities:
            await self._set_state(entity["entity_id"], entity["state"], entity["attributes"])

        self.entities_created = True
        _LOGGER.info("HomeAssistant entities created successfully")

    async def _set_state(self, entity_id: str, state: str, attributes: Dict[str, Any]) -> bool:
        """Set entity state in HomeAssistant."""
        try:
            url = f"{self.ha_url}/api/states/{entity_id}"
            payload = {
                "state": state,
                "attributes": attributes
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status in [200, 201]:
                        _LOGGER.debug(f"Updated {entity_id} to {state}")
                        return True
                    else:
                        _LOGGER.error(f"Failed to update {entity_id}: {response.status}")
                        return False
        except Exception as e:
            _LOGGER.error(f"Error updating entity {entity_id}: {e}")
            return False

    async def update_receiver_status(self, online: bool, device_info: Optional[Dict] = None):
        """Update receiver online/offline status."""
        state = "on" if online else "off"
        attributes = {
            "friendly_name": "ADS-B Receiver Status",
            "device_class": "connectivity",
            "icon": "mdi:airplane" if online else "mdi:airplane-off",
        }

        if device_info:
            attributes["device_type"] = device_info.get("type", "unknown")
            attributes["host"] = device_info.get("host", "unknown")
            attributes["port"] = device_info.get("port", 0)

        await self._set_state("binary_sensor.adsb_receiver", state, attributes)

        # Update location and type sensors
        if device_info:
            location = f"{device_info.get('host', 'unknown')}:{device_info.get('port', 0)}"
            await self._set_state(
                "sensor.adsb_receiver_location",
                location,
                {"friendly_name": "Receiver Location", "icon": "mdi:map-marker-radius"}
            )

            await self._set_state(
                "sensor.adsb_receiver_type",
                device_info.get("type", "unknown"),
                {"friendly_name": "Receiver Type", "icon": "mdi:chip"}
            )

    async def update_aircraft_data(self, aircraft_data: Optional[Dict]):
        """Update aircraft statistics from ADS-B data."""
        if not aircraft_data:
            await self._set_state(
                "sensor.adsb_aircraft_count",
                "0",
                {
                    "friendly_name": "Visible Aircraft",
                    "unit_of_measurement": "aircraft",
                    "icon": "mdi:airplane-clock"
                }
            )
            await self._set_state(
                "sensor.adsb_message_rate",
                "0",
                {
                    "friendly_name": "Message Rate",
                    "unit_of_measurement": "msg/s",
                    "icon": "mdi:radio-tower"
                }
            )
            return

        # Extract aircraft count
        aircraft_count = 0
        if "aircraft" in aircraft_data:
            # Count only aircraft with position
            aircraft_count = sum(
                1 for ac in aircraft_data["aircraft"]
                if "lat" in ac and "lon" in ac
            )

        # Extract message rate (if available)
        message_rate = 0
        if "messages" in aircraft_data:
            message_rate = aircraft_data.get("messages", 0)

        # Update entities
        await self._set_state(
            "sensor.adsb_aircraft_count",
            str(aircraft_count),
            {
                "friendly_name": "Visible Aircraft",
                "unit_of_measurement": "aircraft",
                "icon": "mdi:airplane-clock",
                "total_aircraft": len(aircraft_data.get("aircraft", []))
            }
        )

        await self._set_state(
            "sensor.adsb_message_rate",
            str(message_rate),
            {
                "friendly_name": "Message Rate",
                "unit_of_measurement": "msg/s",
                "icon": "mdi:radio-tower"
            }
        )
