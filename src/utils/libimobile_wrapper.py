#!/usr/bin/env python3
"""
libimobile_wrapper.py - Wrapper for libimobiledevice functionality

This module provides a Python wrapper around libimobiledevice functionality,
making it easier to interact with iOS devices in various states.
"""

import os
import sys
import time
import subprocess
import logging
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeviceError(Exception):
    """Exception raised for device communication errors"""
    pass

class DeviceNotFoundError(DeviceError):
    """Exception raised when no device is found"""
    pass

class DeviceMode(Enum):
    """Enumeration of device modes"""
    NORMAL = 1
    RECOVERY = 2
    DFU = 3
    RESTORE = 4
    UNKNOWN = 5

class LibimobileWrapper:
    """Wrapper class for libimobiledevice functionality"""
    
    def __init__(self, debug: bool = False):
        """
        Initialize the wrapper
        
        Args:
            debug: Whether to enable debug logging
        """
        self.debug = debug
        if debug:
            logger.setLevel(logging.DEBUG)
    
    def _run_command(self, command: List[str]) -> Tuple[int, str, str]:
        """
        Run a shell command
        
        Args:
            command: Command to run as a list of strings
            
        Returns:
            Tuple[int, str, str]: Return code, stdout, stderr
        """
        if self.debug:
            logger.debug(f"Running command: {' '.join(command)}")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        except Exception as e:
            logger.error(f"Error running command: {e}")
            return -1, "", str(e)
    
    def list_devices(self) -> List[str]:
        """
        List connected iOS devices
        
        Returns:
            List[str]: List of device UDIDs
        """
        returncode, stdout, stderr = self._run_command(["idevice_id", "-l"])
        
        if returncode != 0:
            logger.error(f"Error listing devices: {stderr}")
            return []
        
        devices = [line.strip() for line in stdout.splitlines() if line.strip()]
        return devices
    
    def get_device_info(self, udid: Optional[str] = None) -> Dict[str, str]:
        """
        Get information about a device
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            
        Returns:
            Dict[str, str]: Device information
            
        Raises:
            DeviceNotFoundError: If no device is found
        """
        # If no UDID provided, use the first device
        if udid is None:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")
            udid = devices[0]
        
        # Get device name
        returncode, stdout, stderr = self._run_command(["idevicename", "-u", udid])
        device_name = stdout.strip() if returncode == 0 else "Unknown"
        
        # Get device information
        returncode, stdout, stderr = self._run_command(["ideviceinfo", "-u", udid])
        
        if returncode != 0:
            logger.error(f"Error getting device info: {stderr}")
            raise DeviceError(f"Failed to get device info: {stderr}")
        
        # Parse device information
        info = {"udid": udid, "name": device_name}
        for line in stdout.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip()] = value.strip()
        
        return info
    
    def get_device_mode(self, udid: Optional[str] = None) -> DeviceMode:
        """
        Get the current mode of a device
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            
        Returns:
            DeviceMode: The current mode of the device
            
        Raises:
            DeviceNotFoundError: If no device is found
        """
        # If no UDID provided, use the first device
        if udid is None:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")
            udid = devices[0]
        
        # Try to get device info
        try:
            info = self.get_device_info(udid)
            return DeviceMode.NORMAL
        except DeviceError:
            # Device is not in normal mode, check if in recovery
            returncode, stdout, stderr = self._run_command(["irecovery", "-q"])
            if returncode == 0:
                # Check if in DFU or recovery mode
                if "DFU" in stdout:
                    return DeviceMode.DFU
                elif "Recovery" in stdout:
                    return DeviceMode.RECOVERY
                else:
                    return DeviceMode.RESTORE
            
            return DeviceMode.UNKNOWN
    
    def enter_recovery_mode(self, udid: Optional[str] = None) -> bool:
        """
        Put a device into recovery mode
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DeviceNotFoundError: If no device is found
        """
        # If no UDID provided, use the first device
        if udid is None:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")
            udid = devices[0]
        
        # Put device in recovery mode
        returncode, stdout, stderr = self._run_command(["ideviceenterrecovery", udid])
        
        if returncode != 0:
            logger.error(f"Error entering recovery mode: {stderr}")
            return False
        
        return True
    
    def exit_recovery_mode(self, udid: Optional[str] = None) -> bool:
        """
        Exit recovery mode
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Exit recovery mode
        returncode, stdout, stderr = self._run_command(["irecovery", "-n"])
        
        if returncode != 0:
            logger.error(f"Error exiting recovery mode: {stderr}")
            return False
        
        return True
    
    def read_system_logs(self, udid: Optional[str] = None) -> List[str]:
        """
        Read system logs from a device
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            
        Returns:
            List[str]: System logs
            
        Raises:
            DeviceNotFoundError: If no device is found
        """
        # If no UDID provided, use the first device
        if udid is None:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")
            udid = devices[0]
        
        # Read system logs
        returncode, stdout, stderr = self._run_command(["idevicesyslog", "-u", udid])
        
        if returncode != 0:
            logger.error(f"Error reading system logs: {stderr}")
            return []
        
        return stdout.splitlines()
    
    def mount_filesystem(self, udid: Optional[str] = None, read_only: bool = True) -> bool:
        """
        Mount the device filesystem
        
        Args:
            udid: Device UDID (optional, uses first device if not specified)
            read_only: Whether to mount in read-only mode
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DeviceNotFoundError: If no device is found
        """
        # If no UDID provided, use the first device
        if udid is None:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")
            udid = devices[0]
        
        # Mount filesystem
        command = ["ifuse", "--udid", udid]
        if read_only:
            command.append("--read-only")
        command.append("/tmp/iphone-mount")
        
        # Create mount point if it doesn't exist
        os.makedirs("/tmp/iphone-mount", exist_ok=True)
        
        returncode, stdout, stderr = self._run_command(command)
        
        if returncode != 0:
            logger.error(f"Error mounting filesystem: {stderr}")
            return False
        
        return True
    
    def unmount_filesystem(self) -> bool:
        """
        Unmount the device filesystem
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Unmount filesystem
        returncode, stdout, stderr = self._run_command(["fusermount", "-u", "/tmp/iphone-mount"])
        
        if returncode != 0:
            logger.error(f"Error unmounting filesystem: {stderr}")
            return False
        
        return True

# Example usage
if __name__ == "__main__":
    wrapper = LibimobileWrapper(debug=True)
    
    try:
        devices = wrapper.list_devices()
        print(f"Found {len(devices)} devices: {devices}")
        
        if devices:
            udid = devices[0]
            info = wrapper.get_device_info(udid)
            print(f"\nDevice information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            mode = wrapper.get_device_mode(udid)
            print(f"\nDevice mode: {mode.name}")
    except DeviceError as e:
        print(f"Error: {e}")
