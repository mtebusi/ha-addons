# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-11-12

### Added
- Initial release of ADS-B Dashboard add-on
- Automatic network scanning for ADS-B receivers
- Support for multiple ADS-B receiver types (PiAware, dump1090, readsb, tar1090, ADSBexchange)
- tar1090 dashboard integration with automatic updates
- Home Assistant entity integration:
  - Binary sensor for receiver status
  - Sensors for aircraft count, message rate, receiver type, and location
- Nginx proxy for dashboard and data forwarding
- AppArmor security profile
- Multi-architecture support (amd64, aarch64, armv7, armhf, i386)
- Lazy loading for performance optimization
- Configurable scan intervals
- Manual device configuration option
- Comprehensive documentation

### Features
- Zero-configuration auto-discovery
- One-click installation
- Remote access support via Home Assistant Ingress
- Lightweight design (~50MB memory footprint)
- Optimized for low-power hardware

### Security
- Restrictive AppArmor profile
- Local network only access
- No external data transmission
- Non-root execution

## [Unreleased]

### Planned
- Multiple receiver support
- Historical aircraft data logging
- Custom alert configurations
- Enhanced statistics and graphs
- MLAT integration
- Aircraft database integration
