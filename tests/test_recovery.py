#!/usr/bin/env python3
"""
test_recovery.py - Tests for the recovery tool

This module contains tests for the recovery tool functionality.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.DiagnosticTool import BootLoopCause, DeviceInfo
from src.core.RecoveryTool import RecoveryTool, RecoveryMethod, RecoveryResult

class TestRecoveryTool(unittest.TestCase):
    """Tests for the RecoveryTool class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create test device info
        self.device_info = DeviceInfo()
        self.device_info.model = "iPhone XS"
        self.device_info.chip = "A12 Bionic"
        self.device_info.ios_version = "15.4.1"
        self.device_info.in_recovery_mode = True
        
        # Create recovery tool
        self.recovery = RecoveryTool(self.device_info)
    
    def test_force_restart(self):
        """Test force restart method"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.recovery.force_restart()
            
            # Check result
            self.assertEqual(result, RecoveryResult.FAILURE)
            
            # Check logs
            self.assertGreater(len(self.recovery.recovery_logs), 0)
            self.assertIn("Force restart", self.recovery.recovery_logs[0])
    
    def test_targeted_repair_corrupted_files(self):
        """Test targeted repair for corrupted system files"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.recovery.targeted_repair(BootLoopCause.CORRUPTED_SYSTEM_FILES)
            
            # Check result
            self.assertEqual(result, RecoveryResult.SUCCESS)
            
            # Check logs
            self.assertGreater(len(self.recovery.recovery_logs), 0)
            self.assertIn("Targeting system file corruption", self.recovery.recovery_logs[1])
    
    def test_targeted_repair_other_cause(self):
        """Test targeted repair for other causes"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.recovery.targeted_repair(BootLoopCause.HARDWARE_FAILURE)
            
            # Check result
            self.assertEqual(result, RecoveryResult.FAILURE)
            
            # Check logs
            self.assertGreater(len(self.recovery.recovery_logs), 0)
            self.assertIn("not available", self.recovery.recovery_logs[1].lower())
    
    def test_system_reset(self):
        """Test system reset method"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.recovery.system_reset()
            
            # Check result
            self.assertEqual(result, RecoveryResult.SUCCESS)
            
            # Check logs
            self.assertGreater(len(self.recovery.recovery_logs), 0)
            self.assertIn("system partition reset", self.recovery.recovery_logs[0].lower())
    
    def test_dfu_restore(self):
        """Test DFU restore method"""
        # Mock time.sleep to avoid delays
        with patch('time.sleep'):
            result = self.recovery.dfu_restore()
            
            # Check result
            self.assertEqual(result, RecoveryResult.SUCCESS)
            
            # Check logs
            self.assertGreater(len(self.recovery.recovery_logs), 0)
            self.assertIn("DFU restore", self.recovery.recovery_logs[0])
            self.assertIn("WARNING", self.recovery.recovery_logs[0])

if __name__ == '__main__':
    unittest.main()
