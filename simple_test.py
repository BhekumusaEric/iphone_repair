#!/usr/bin/env python3
"""
simple_test.py - Simple test for device connectivity
"""

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Import device communication classes
from utils.device_communication import DeviceCommunication

def check_command_exists(command):
    """Check if a command exists in the PATH"""
    try:
        result = subprocess.run(
            ["which", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def main():
    """Main function"""
    print("Testing device connectivity...")

    # Check for required commands
    print("\nChecking for required commands:")
    commands = ["idevice_id", "ideviceinfo", "idevicename", "idevicesyslog"]
    missing_commands = []

    for command in commands:
        exists = check_command_exists(command)
        print(f"  {command}: {'Found' if exists else 'Not found'}")
        if not exists:
            missing_commands.append(command)

    # Check if libimobiledevice is installed
    if missing_commands:
        print("\nWARNING: Some required commands are missing.")
        print("For real device communication, please install libimobiledevice:")
        print("\n  On Ubuntu/Debian:")
        print("  sudo apt-get install libimobiledevice-utils libusbmuxd-tools ifuse")
        print("\n  On macOS:")
        print("  brew install libimobiledevice")
        print("\nFalling back to simulation mode...")
        simulate = True
    else:
        print("\nAll required commands found. Using real device communication.")
        simulate = False

    # Create device communication
    print(f"\nInitializing device communication (simulate={simulate})...")
    comm = DeviceCommunication(simulate=simulate, debug=True)

    # Detect devices
    print("Detecting devices...")
    devices = comm.detect_devices()

    print(f"\nDetected {len(devices)} device(s):")
    if not devices:
        print("  No devices detected.")
        if not simulate:
            print("\nTroubleshooting tips:")
            print("  1. Check USB connection")
            print("  2. Make sure device is not locked")
            print("  3. Try unplugging and reconnecting the device")
            print("  4. Check if device is recognized by the system:")
            print("     - On Linux: run 'lsusb' to see if device is listed")
            print("     - On macOS: run 'system_profiler SPUSBDataType' to see if device is listed")
    else:
        for i, device in enumerate(devices, 1):
            print(f"\nDevice {i}:")
            print(f"  Name: {device.get('name', 'Unknown')}")
            print(f"  Model: {device.get('model', 'Unknown')}")
            print(f"  Mode: {device.get('mode', 'Unknown')}")

            # Try to get device info
            try:
                print("\n  Getting detailed device info...")
                info = comm.get_device_info(device['udid'])
                print("  Device info:")
                for key, value in info.items():
                    if key not in ['udid', 'name', 'model', 'mode']:
                        print(f"    {key}: {value}")
            except Exception as e:
                print(f"  Error getting device info: {e}")

    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
