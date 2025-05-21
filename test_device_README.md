# iPhone Device Testing Tool

This tool allows you to test the device connectivity functionality of the iPhone Boot Recovery Tool. It can detect connected devices, display device information, and perform basic operations like entering and exiting recovery mode.

## Prerequisites

- Python 3.6 or higher
- For real device communication:
  - libimobiledevice utilities (`libimobiledevice-utils`, `libusbmuxd-tools`, `ifuse`)

## Installation

### Installing libimobiledevice (for real device communication)

On Ubuntu/Debian:
```bash
sudo apt-get install libimobiledevice-utils libusbmuxd-tools ifuse
```

On macOS:
```bash
brew install libimobiledevice
```

## Usage

Basic usage:
```bash
python3 test_device.py
```

### Command-line Options

- `--simulate`: Run in simulation mode without actual device communication
- `--debug`: Enable debug logging
- `--recovery`: Attempt to put device in recovery mode (use with caution)
- `--exit-recovery`: Attempt to exit recovery mode (use with caution)
- `--logs`: Show full system logs (if available)

### Examples

Test device connectivity in simulation mode:
```bash
python3 test_device.py --simulate
```

Test device connectivity with debug logging:
```bash
python3 test_device.py --debug
```

Attempt to put device in recovery mode:
```bash
python3 test_device.py --recovery
```

Attempt to exit recovery mode:
```bash
python3 test_device.py --exit-recovery
```

Show full system logs:
```bash
python3 test_device.py --logs
```

## Troubleshooting

If you encounter issues with real device communication:

1. Make sure libimobiledevice utilities are installed
2. Check USB connection
3. Try running with `--debug` flag for more information
4. Ensure your device is not in a locked state
5. On Linux, check udev rules for device access

## Notes

- The tool will automatically fall back to simulation mode if libimobiledevice utilities are not found
- Recovery mode operations should be used with caution
- System logs are only available for devices in normal mode
