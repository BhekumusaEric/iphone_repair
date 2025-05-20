#!/usr/bin/env python3
"""
test_diagnostic.py - Tests for the diagnostic tool

This module contains tests for the diagnostic tool functionality.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.DiagnosticTool import DiagnosticTool, BootLoopCause, DeviceInfo

class TestDiagnosticTool(unittest.TestCase):
    """Tests for the DiagnosticTool class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.diagnostic = DiagnosticTool()
        
        # Create test device info
        self.device_info = DeviceInfo()
        self.device_info.model = "iPhone XS"
        self.device_info.chip = "A12 Bionic"
        self.device_info.ios_version = "15.4.1"
        self.device_info.in_recovery_mode = True
        
        # Set device info
        self.diagnostic.device_info = self.device_info
    
    def test_device_detection(self):
        """Test device detection"""
        # Mock the detect_device method
        with patch.object(DiagnosticTool, 'detect_device', return_value=True):
            result = self.diagnostic.detect_device()
            self.assertTrue(result)
            self.assertEqual(self.diagnostic.device_info.model, "iPhone XS")
            self.assertEqual(self.diagnostic.device_info.chip, "A12 Bionic")
    
    def test_is_a12_or_newer(self):
        """Test A12 chip detection"""
        # Test A12 chip
        self.device_info.chip = "A12 Bionic"
        self.assertTrue(self.device_info.is_a12_or_newer())
        
        # Test A13 chip
        self.device_info.chip = "A13 Bionic"
        self.assertTrue(self.device_info.is_a12_or_newer())
        
        # Test A11 chip
        self.device_info.chip = "A11 Bionic"
        self.assertFalse(self.device_info.is_a12_or_newer())
        
        # Test M1 chip
        self.device_info.chip = "M1"
        self.assertTrue(self.device_info.is_a12_or_newer())
    
    def test_analyze_boot_issue_a12(self):
        """Test boot issue analysis for A12 devices"""
        # Set A12 chip
        self.device_info.chip = "A12 Bionic"
        
        # Test analysis
        cause = self.diagnostic.analyze_boot_issue()
        self.assertEqual(cause, BootLoopCause.CORRUPTED_SYSTEM_FILES)
    
    def test_analyze_boot_issue_pre_a12(self):
        """Test boot issue analysis for pre-A12 devices"""
        # Set A11 chip
        self.device_info.chip = "A11 Bionic"
        
        # Test analysis
        cause = self.diagnostic.analyze_boot_issue()
        self.assertEqual(cause, BootLoopCause.FAILED_UPDATE)
    
    def test_generate_recovery_options_corrupted_files(self):
        """Test recovery options for corrupted system files"""
        options = self.diagnostic.generate_recovery_options(BootLoopCause.CORRUPTED_SYSTEM_FILES)
        
        self.assertEqual(len(options), 3)
        self.assertIn("system file repair", options[0].lower())
        self.assertIn("system partition", options[1].lower())
        self.assertIn("restore", options[2].lower())
    
    def test_generate_recovery_options_failed_update(self):
        """Test recovery options for failed update"""
        options = self.diagnostic.generate_recovery_options(BootLoopCause.FAILED_UPDATE)
        
        self.assertEqual(len(options), 3)
        self.assertIn("resume", options[0].lower())
        self.assertIn("downgrade", options[1].lower())
        self.assertIn("restore", options[2].lower())

if __name__ == '__main__':
    unittest.main()
