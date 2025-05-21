# iPhone Boot Recovery Tool

A comprehensive solution for recovering iPhones stuck on the Apple logo, with special focus on A12 chip devices (iPhone XS, XR and newer).

## Problem Statement

Many iPhone users experience their devices getting stuck on the Apple logo during boot, commonly known as a "boot loop." Traditional recovery methods often result in complete data loss, causing significant frustration for users.

## Our Solution

This tool provides a multi-layered approach to recovering iPhones from boot loops:

1. **Non-invasive Recovery**: Attempts to recover the device without data loss
2. **Diagnostic Analysis**: Identifies the specific cause of the boot loop
3. **Guided Recovery**: Step-by-step instructions for various recovery methods
4. **Data Preservation**: Prioritizes solutions that maintain user data when possible
5. **Advanced Techniques**: Implements sophisticated recovery methods for complex issues

## Technical Approach

- Communication with devices in Recovery/DFU mode using libimobiledevice
- Safe system file modification techniques
- Custom firmware patching for A12+ devices
- User-friendly interface for non-technical users
- Advanced filesystem repair utilities

## Features

- **Diagnostic Engine**: Precisely identifies the cause of boot loops
- **Multiple Recovery Methods**: From simple force restart to advanced firmware patching
- **Dual Interface**: Both command-line and graphical user interfaces
- **Device Simulation**: Test mode for development and demonstration
- **Comprehensive Testing**: Extensive test suite for reliability
- **Ultimate Recovery**: Last-resort option that prioritizes device access over security (may bypass restrictions)
- **Inheritance Support**: Guidance and documentation for accessing inherited devices through Apple's official process

## Target Devices

- Primary focus: iPhone XS, XR, and newer (A12 chip and above)
- Secondary support: Older iPhone models (A11 and below)

## Usage

```bash
# Basic usage with CLI
python main.py

# Use GUI interface (if PyQt5 is installed)
python main.py --gui

# Run in simulation mode (no real device needed)
python main.py --simulate

# Enable advanced recovery techniques
python main.py --advanced

# Enable ultimate recovery mode (last resort)
python main.py --ultimate

# Access inheritance support for devices with unknown credentials
python main.py --inheritance

# Run tests
python main.py --test

# Enable debug logging
python main.py --debug
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BhekumusaEric/iphone_repair.git
   cd iphone_repair
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. For real device communication, install libimobiledevice:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install libimobiledevice-utils libusbmuxd-tools ifuse

   # On macOS
   brew install libimobiledevice
   ```

## Potential for Apple Integration

This solution could be integrated into Apple's existing recovery tools:
- As a feature in iTunes/Finder
- As a standalone recovery application
- As part of Apple Store Genius Bar diagnostic tools

## Development Status

This project is currently in active development. See the [technical details](src/docs/technical_details.md) for more information about the implementation.
