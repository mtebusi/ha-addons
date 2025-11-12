# ADS-B Dashboard Add-on Documentation

## Overview

The ADS-B Dashboard add-on transforms your Home Assistant instance into a powerful aircraft tracking station by automatically discovering and integrating with ADS-B receivers on your local network.

## Features

### Automatic Discovery

The add-on automatically scans your local network for ADS-B receivers, including:

- **PiAware** (FlightAware's dump1090-fa)
- **dump1090** and **dump1090-mutability**
- **readsb**
- **tar1090**
- **ADSBexchange feeders**
- Any receiver serving data on standard ports (30002-30005, 30104, 8080)

No configuration required - just install and go!

### tar1090 Dashboard

Get a full-featured aircraft tracking interface with:

- Real-time aircraft positions on an interactive map
- Flight tracks and history
- Aircraft details (callsign, altitude, speed, heading)
- Range circles and statistics
- Multiple map layers
- Dark mode support

The dashboard automatically updates from the official tar1090 repository on startup.

### Home Assistant Integration

The add-on creates native Home Assistant entities that you can use in automations, dashboards, and scripts:

#### Binary Sensor: ADS-B Receiver
- **Entity ID**: `binary_sensor.adsb_receiver`
- **States**: `on` (online) or `off` (offline)
- **Use case**: Get notifications when your ADS-B receiver goes offline

Example automation:
```yaml
automation:
  - alias: "ADS-B Receiver Offline Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.adsb_receiver
        to: 'off'
        for: '00:05:00'
    action:
      - service: notify.mobile_app
        data:
          message: "ADS-B receiver has been offline for 5 minutes"
```

#### Sensor: Aircraft Count
- **Entity ID**: `sensor.adsb_aircraft_count`
- **Unit**: aircraft
- **Use case**: Track how many aircraft are currently visible

Example card:
```yaml
type: entity
entity: sensor.adsb_aircraft_count
name: Visible Aircraft
icon: mdi:airplane
```

#### Sensor: Message Rate
- **Entity ID**: `sensor.adsb_message_rate`
- **Unit**: msg/s
- **Use case**: Monitor receiver performance

#### Sensor: Receiver Type
- **Entity ID**: `sensor.adsb_receiver_type`
- **Use case**: Display what type of receiver is connected

#### Sensor: Receiver Location
- **Entity ID**: `sensor.adsb_receiver_location`
- **Use case**: Show the IP address and port of your receiver

## Configuration Options

### Basic Configuration

The add-on works with zero configuration, but you can customize it:

```yaml
log_level: info
scan_interval: 30
auto_detect: true
manual_host: ""
manual_port: 0
update_tar1090: true
```

### Advanced: Manual Configuration

If you have a static IP for your ADS-B receiver or want to disable auto-discovery:

```yaml
log_level: info
scan_interval: 60
auto_detect: false
manual_host: "192.168.1.100"
manual_port: 8080
update_tar1090: true
```

## Network Requirements

### Firewall Rules

The add-on needs to:
- Scan your local network (no external access required)
- Connect to your ADS-B receiver on HTTP ports (typically 8080)
- Access GitHub for tar1090 updates (can be disabled)

### Supported ADS-B Ports

The scanner checks these common ports:
- **30002**: Raw output port
- **30003**: BaseStation format
- **30005**: Beast format
- **30104**: Beast format with timestamps
- **8080**: HTTP web interface
- **8081**: Alternative HTTP port
- **80**: Standard HTTP port

## Remote Access

The dashboard works seamlessly with Home Assistant's remote access solutions:

### Nabu Casa (Home Assistant Cloud)
The add-on uses Home Assistant Ingress, so it automatically works with Nabu Casa remote access.

### Manual Remote Access
If you're using a reverse proxy (nginx, Caddy, etc.), the dashboard will work automatically through your existing Home Assistant remote access setup.

## Performance Optimization

The add-on is designed for low-power hardware:

### Lazy Loading
The dashboard only establishes connections to your ADS-B receiver when you're actively viewing it, saving bandwidth and processing power.

### Efficient Scanning
Network scanning uses asynchronous I/O to minimize CPU usage and complete quickly.

### Memory Footprint
Typical memory usage: ~50MB

### Scan Interval
Adjust `scan_interval` based on your needs:
- **10-20 seconds**: If your receiver moves or restarts frequently
- **30 seconds**: Default, good balance
- **60+ seconds**: For stable setups to reduce network traffic

## Troubleshooting

### No Device Found

If the add-on can't find your ADS-B receiver:

1. **Check the receiver is online**: Can you access it directly at `http://<ip>:8080`?
2. **Verify network connectivity**: Make sure the receiver is on the same network as Home Assistant
3. **Check firewall rules**: Ensure ports 8080, 30003, 30005 are not blocked
4. **Use manual configuration**: Set `auto_detect: false` and specify the IP/port manually

### Dashboard Not Loading

1. **Check logs**: Look at the add-on logs for errors
2. **Verify tar1090 update**: Set `update_tar1090: true` and restart
3. **Check nginx**: The proxy service should be running (check logs)

### Entities Not Appearing

1. **Restart Home Assistant**: Sometimes entities need a restart to appear
2. **Check Supervisor API**: The add-on needs `homeassistant_api: true` (already set)
3. **Review logs**: Look for errors related to "entity" or "state"

### Performance Issues

1. **Increase scan_interval**: Set to 60 or higher
2. **Check network speed**: Slow networks may timeout during scanning
3. **Verify receiver performance**: Check if the ADS-B receiver itself is slow

## Security

### AppArmor Profile

The add-on uses a restrictive AppArmor profile that:
- Limits network access to local network only
- Restricts file system access
- Prevents privilege escalation

### Local Network Only

The add-on only accesses:
- Your local network for scanning
- Your ADS-B receiver for data
- GitHub for tar1090 updates (optional)

No ADS-B data is sent externally.

## Example Dashboard Card

Add this to your Home Assistant dashboard:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: ADS-B Receiver
    entities:
      - entity: binary_sensor.adsb_receiver
        name: Status
      - entity: sensor.adsb_receiver_type
        name: Type
      - entity: sensor.adsb_receiver_location
        name: Location
  - type: glance
    title: Aircraft Statistics
    entities:
      - entity: sensor.adsb_aircraft_count
        name: Visible Aircraft
      - entity: sensor.adsb_message_rate
        name: Message Rate
  - type: iframe
    url: /api/hassio_ingress/<token>
    aspect_ratio: 16:9
    title: Live Aircraft Map
```

## Credits

This add-on integrates several excellent open-source projects:

- **[tar1090](https://github.com/wiedehopf/tar1090)** - Beautiful web interface for aircraft tracking
- **[dump1090](https://github.com/flightaware/dump1090)** - Mode S decoder for ADS-B data
- **[Home Assistant](https://www.home-assistant.io/)** - Open source home automation platform

Special thanks to the ADS-B community for their continued development and support!

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/mtebusi/ha-addons/issues)
- **Community**: Join the Home Assistant community forums
- **Documentation**: Check the [tar1090 documentation](https://github.com/wiedehopf/tar1090) for dashboard features

## License

This add-on is licensed under the MIT License. See LICENSE file for details.
