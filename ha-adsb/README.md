# ADS-B Dashboard for Home Assistant

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

A lightweight Home Assistant add-on that automatically discovers ADS-B receivers on your local network and provides a beautiful tar1090 dashboard with real-time aircraft tracking.

## About

This add-on scans your local network for ADS-B receivers (such as PiAware, dump1090, readsb, or ADSBexchange feeders) and automatically integrates them with Home Assistant. It provides:

- **Automatic Discovery**: Scans your network and finds ADS-B receivers without configuration
- **Real-time Dashboard**: Full tar1090 interface accessible through Home Assistant
- **Home Assistant Integration**: Entities for receiver status, aircraft count, and message rate
- **Remote Access**: Access your ADS-B data remotely via Nabu Casa or your preferred remote access method
- **Lightweight**: Optimized for performance on low-power hardware
- **Auto-updates**: Automatically updates tar1090 to the latest version

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "ADS-B Dashboard" add-on
3. Start the add-on
4. That's it! The add-on will automatically detect your ADS-B receiver

## Configuration

The add-on works out-of-the-box with zero configuration, but you can customize it if needed:

```yaml
log_level: info
scan_interval: 30
auto_detect: true
manual_host: ""
manual_port: 0
update_tar1090: true
```

### Option: `log_level`

The `log_level` option controls the level of log output by the add-on.

### Option: `scan_interval`

How often (in seconds) to scan the network for ADS-B devices. Default is 30 seconds.

### Option: `auto_detect`

Enable automatic detection of ADS-B receivers on your network. Set to `false` if you want to manually specify a device.

### Option: `manual_host`

If `auto_detect` is `false`, specify the IP address of your ADS-B receiver here.

### Option: `manual_port`

If `auto_detect` is `false`, specify the port of your ADS-B receiver here (usually 8080).

### Option: `update_tar1090`

Automatically update tar1090 to the latest version on startup. Default is `true`.

## Home Assistant Entities

The add-on creates the following entities:

- `binary_sensor.adsb_receiver`: Online/offline status of your ADS-B receiver
- `sensor.adsb_aircraft_count`: Number of aircraft currently visible
- `sensor.adsb_message_rate`: Messages per second from the receiver
- `sensor.adsb_receiver_type`: Type of ADS-B receiver detected (piaware, dump1090, etc.)
- `sensor.adsb_receiver_location`: IP address and port of the receiver

## Dashboard Access

Once the add-on is running, you can access the tar1090 dashboard through:

1. The "ADS-B Dashboard" panel in Home Assistant's sidebar
2. The Ingress interface in the add-on page

The dashboard will show real-time aircraft positions, tracks, and statistics.

## Support

For issues and feature requests, please open an issue on [GitHub](https://github.com/mtebusi/ha-addons/issues).

## Credits

- [tar1090](https://github.com/wiedehopf/tar1090) by wiedehopf
- [dump1090](https://github.com/flightaware/dump1090) by FlightAware
- All the amazing ADS-B community contributors

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
