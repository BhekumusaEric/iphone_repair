#!/usr/bin/env python3
"""
test_device_communication.py - Tests for the device communication module

This module contains tests for the device communication functionality.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.device_communication import DeviceCommunication, DeviceMode

class TestDeviceCommunication(unittest.TestCase):
    """Tests for the DeviceCommunication class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create device communication with simulation mode
        self.comm = DeviceCommunication(simulate=True)
    
    def test_detect_devices_simulation(self):
        """Test device detection in simulation mode"""
        devices = self.comm.detect_devices()
        
        # Check devices
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["model"], "iPhone12,3")
        self.assertEqual(devices[0]["mode"], DeviceMode.RECOVERY.name)
    
    def test_get_device_mode_simulation(self):
        """Test getting device mode in simulation mode"""
        mode = self.comm.get_device_mode("00000000-0000000000000000")
        
        # Check mode
        self.assertEqual(mode, DeviceMode.RECOVERY)
    
    def test_enter_recovery_mode_simulation(self):
        """Test entering recovery mode in simulation mode"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.comm.enter_recovery_mode("00000000-0000000000000000")
            
            # Check result
            self.assertTrue(result)
    
    def test_exit_recovery_mode_simulation(self):
        """Test exiting recovery mode in simulation mode"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.comm.exit_recovery_mode("00000000-0000000000000000")
            
            # Check result
            self.assertTrue(result)
    
    def test_get_device_info_simulation(self):
        """Test getting device info in simulation mode"""
        info = self.comm.get_device_info("00000000-0000000000000000")
        
        # Check info
        self.assertEqual(info["model"], "iPhone12,3")
        self.assertEqual(info["chip_id"], "0x8020")
        self.assertEqual(info["firmware_version"], "15.4.1")
    
    def test_read_system_logs_simulation(self):
        """Test reading system logs in simulation mode"""
        logs = self.comm.read_system_logs("00000000-0000000000000000")
        
        # Check logs
        self.assertGreater(len(logs), 0)
        self.assertIn("Darwin Kernel Version", logs[0])
    
    def test_mount_filesystem_simulation(self):
        """Test mounting filesystem in simulation mode"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.comm.mount_filesystem("00000000-0000000000000000")
            
            # Check result
            self.assertTrue(result)
    
    def test_unmount_filesystem_simulation(self):
        """Test unmounting filesystem in simulation mode"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.comm.unmount_filesystem("00000000-0000000000000000")
            
            # Check result
            self.assertTrue(result)
    
    @patch('src.utils.device_communication.LibimobileWrapper')
    def test_detect_devices_real(self, mock_wrapper):
        """Test device detection with real wrapper"""
        # Create device communication with real mode
        comm = DeviceCommunication(simulate=False)
        
        # Mock wrapper
        mock_instance = mock_wrapper.return_value
        mock_instance.list_devices.return_value = ["00000000-0000000000000000"]
        mock_instance.get_device_info.return_value = {
            "udid": "00000000-0000000000000000",
            "name": "iPhone",
            "model": "iPhone12,3"
        }
        mock_instance.get_device_mode.return_value = DeviceMode.NORMAL
        
        # Set wrapper
        comm.wrapper = mock_instance
        comm.simulate = False
        
        # Test detection
        devices = comm.detect_devices()
        
        # Check devices
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["model"], "iPhone12,3")
        self.assertEqual(devices[0]["mode"], DeviceMode.NORMAL.name)
        
        # Verify calls
        mock_instance.list_devices.assert_called_once()
        mock_instance.get_device_info.assert_called_once_with("00000000-0000000000000000")
        mock_instance.get_device_mode.assert_called_once_with("00000000-0000000000000000")

if __name__ == '__main__':
    unittest.main()
