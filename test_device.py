#!/usr/bin/env python3
"""
test_device.py - Test device connectivity and display device information

This script tests the device connectivity functionality of the iPhone Boot Recovery Tool.
It attempts to detect connected devices and display information about them.
"""

import os
import sys
import argparse
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Import device communication classes
from utils.device_communication import DeviceCommunication, DeviceMode, DeviceError, DeviceNotFoundError

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Test device connectivity and display device information"
    )

    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Run in simulation mode without actual device communication"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "--recovery",
        action="store_true",
        help="Attempt to put device in recovery mode (use with caution)"
    )

    parser.add_argument(
        "--exit-recovery",
        action="store_true",
        help="Attempt to exit recovery mode (use with caution)"
    )

    parser.add_argument(
        "--logs",
        action="store_true",
        help="Show full system logs (if available)"
    )

    return parser.parse_args()

def check_libimobiledevice_installation() -> bool:
    """
    Check if libimobiledevice utilities are installed

    Returns:
        bool: True if installed, False otherwise
    """
    import subprocess

    try:
        # Check for idevice_id command
        result = subprocess.run(
            ["which", "idevice_id"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return result.returncode == 0
    except Exception:
        return False

def test_device_connectivity(
    simulate: bool = False,
    debug: bool = False,
    enter_recovery: bool = False,
    exit_recovery: bool = False,
    show_full_logs: bool = False
) -> None:
    """
    Test device connectivity and display device information

    Args:
        simulate: Whether to use simulation mode
        debug: Whether to enable debug logging
        enter_recovery: Whether to attempt to put device in recovery mode
        exit_recovery: Whether to attempt to exit recovery mode
        show_full_logs: Whether to show full system logs
    """
    # Set debug logging if requested
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Check if libimobiledevice is installed
    if not simulate and not check_libimobiledevice_installation():
        logger.warning("libimobiledevice utilities not found")
        print("\nWARNING: libimobiledevice utilities not found.")
        print("For real device communication, please install libimobiledevice:")
        print("\n  On Ubuntu/Debian:")
        print("  sudo apt-get install libimobiledevice-utils libusbmuxd-tools ifuse")
        print("\n  On macOS:")
        print("  brew install libimobiledevice")
        print("\nFalling back to simulation mode...")
        simulate = True

    # Create device communication
    logger.info("Initializing device communication...")
    comm = DeviceCommunication(simulate=simulate, debug=debug)

    # Detect devices
    logger.info("Detecting connected devices...")
    try:
        devices = comm.detect_devices()

        if not devices:
            logger.warning("No devices detected")
            print("\nNo devices detected. Please check the connection and try again.")
            return

        # Display device information
        print(f"\nDetected {len(devices)} device(s):")

        for i, device in enumerate(devices, 1):
            print(f"\nDevice {i}:")
            print(f"  Name: {device.get('name', 'Unknown')}")
            print(f"  Model: {device.get('model', 'Unknown')}")
            print(f"  Mode: {device.get('mode', 'Unknown')}")

            # Get more information
            try:
                info = comm.get_device_info(device['udid'])

                print("\n  Device Information:")
                for key, value in info.items():
                    if key not in ['udid', 'name', 'model', 'mode']:
                        print(f"    {key}: {value}")

                # Get device mode
                mode = comm.get_device_mode(device['udid'])
                print(f"\n  Current Mode: {mode.name}")

                # Handle recovery mode operations
                if enter_recovery and mode != DeviceMode.RECOVERY:
                    print("\n  Attempting to put device in recovery mode...")
                    try:
                        result = comm.enter_recovery_mode(device['udid'])
                        if result:
                            print("  SUCCESS: Device entered recovery mode")
                        else:
                            print("  FAILED: Could not put device in recovery mode")
                    except DeviceError as e:
                        logger.error(f"Error entering recovery mode: {e}")
                        print(f"  ERROR: {e}")

                if exit_recovery and mode == DeviceMode.RECOVERY:
                    print("\n  Attempting to exit recovery mode...")
                    try:
                        result = comm.exit_recovery_mode(device['udid'])
                        if result:
                            print("  SUCCESS: Device exited recovery mode")
                        else:
                            print("  FAILED: Could not exit recovery mode")
                    except DeviceError as e:
                        logger.error(f"Error exiting recovery mode: {e}")
                        print(f"  ERROR: {e}")

                # Read system logs if in normal mode
                if mode == DeviceMode.NORMAL:
                    logs = comm.read_system_logs(device['udid'])

                    if show_full_logs:
                        print("\n  System Logs:")
                        for log in logs:
                            print(f"    {log}")
                    else:
                        print("\n  System Logs (first 5 lines):")
                        for log in logs[:5]:
                            print(f"    {log}")
                        if len(logs) > 5:
                            print(f"    ... ({len(logs) - 5} more lines, use --logs to see all)")
            except DeviceError as e:
                logger.error(f"Error getting device info: {e}")
                print(f"\n  Error getting device info: {e}")

    except DeviceError as e:
        logger.error(f"Error detecting devices: {e}")
        print(f"\nError detecting devices: {e}")

def main() -> int:
    """Main entry point"""
    args = parse_args()

    try:
        # Check for conflicting options
        if args.recovery and args.exit_recovery:
            print("Error: Cannot use --recovery and --exit-recovery together")
            return 1

        # Test device connectivity
        test_device_connectivity(
            simulate=args.simulate,
            debug=args.debug,
            enter_recovery=args.recovery,
            exit_recovery=args.exit_recovery,
            show_full_logs=args.logs
        )
        return 0
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\nUnexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
