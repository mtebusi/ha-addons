#!/usr/bin/env python3
"""Validate Home Assistant add-on configuration."""
import yaml
import sys
import os
from pathlib import Path


def validate_addon(config_path: str) -> bool:
    """Validate a single add-on configuration."""
    addon_dir = os.path.dirname(config_path)
    addon_name = os.path.basename(addon_dir)

    try:
        # Load and parse config
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Check required fields
        required_fields = ['name', 'version', 'slug', 'description', 'arch']
        for field in required_fields:
            if field not in config:
                print(f"❌ {addon_name}: Missing required field: {field}")
                return False

        # Check required files
        required_files = ['README.md', 'Dockerfile']
        for req_file in required_files:
            file_path = os.path.join(addon_dir, req_file)
            if not os.path.exists(file_path):
                print(f"❌ {addon_name}: Missing required file: {req_file}")
                return False

        print(f"✅ {addon_name}: Configuration valid")
        return True

    except yaml.YAMLError as e:
        print(f"❌ {addon_name}: Invalid YAML: {e}")
        return False
    except Exception as e:
        print(f"❌ {addon_name}: Validation error: {e}")
        return False


def main():
    """Validate all add-on configurations."""
    if len(sys.argv) > 1:
        # Validate specific config file
        result = validate_addon(sys.argv[1])
        sys.exit(0 if result else 1)
    else:
        # Find and validate all configs
        root = Path('.')
        configs = list(root.glob('*/config.yaml'))

        # Filter out .common and templates
        configs = [c for c in configs if '.common' not in str(c) and 'templates' not in str(c)]

        if not configs:
            print("No add-on configurations found")
            sys.exit(1)

        all_valid = True
        for config in configs:
            if not validate_addon(str(config)):
                all_valid = False

        sys.exit(0 if all_valid else 1)


if __name__ == '__main__':
    main()
