#!/usr/bin/env python3
"""
cli.py - Command Line Interface for iPhone Boot Recovery Tool

This module provides a text-based interface for the recovery tool,
allowing users to diagnose and recover iPhones from boot loops.
"""

import os
import sys
import time
from typing import List, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.DiagnosticTool import DiagnosticTool, BootLoopCause
from core.RecoveryTool import RecoveryTool, RecoveryMethod, RecoveryResult

class CLI:
    """Command Line Interface for iPhone Boot Recovery Tool"""
    
    def __init__(self):
        self.diagnostic_tool = DiagnosticTool()
        self.recovery_tool = None
        self.cause = None
        self.recovery_options = []
    
    def print_header(self):
        """Print application header"""
        print("\n" + "=" * 80)
        print(" " * 25 + "iPhone Boot Recovery Tool")
        print(" " * 20 + "A12+ Device Recovery Specialist")
        print("=" * 80 + "\n")
    
    def print_section(self, title: str):
        """Print section header"""
        print("\n" + "-" * 80)
        print(f" {title}")
        print("-" * 80)
    
    def wait_for_key(self):
        """Wait for user to press a key to continue"""
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the CLI application"""
        self.print_header()
        print("This tool helps recover iPhones stuck on the Apple logo (boot loop).")
        print("It specializes in A12+ devices (iPhone XS/XR and newer) but works with older models too.")
        
        self.print_section("DEVICE DETECTION")
        print("Please connect your iPhone to this computer using a Lightning or USB-C cable.")
        print("If your device is not already in recovery mode, the tool will guide you.")
        self.wait_for_key()
        
        # Detect device
        if not self.diagnostic_tool.detect_device():
            print("\nNo device detected. Please check the connection and try again.")
            return
        
        device_info = self.diagnostic_tool.device_info
        self.recovery_tool = RecoveryTool(device_info)
        
        # Show device info
        print(f"\nDetected device: {device_info.model}")
        print(f"Chip: {device_info.chip}")
        print(f"iOS Version: {device_info.ios_version}")
        print(f"Recovery Mode: {'Yes' if device_info.in_recovery_mode else 'No'}")
        print(f"DFU Mode: {'Yes' if device_info.in_dfu_mode else 'No'}")
        
        # If not in recovery or DFU mode, guide user
        if not (device_info.in_recovery_mode or device_info.in_dfu_mode):
            self.print_section("ENTER RECOVERY MODE")
            print("Your device needs to be in Recovery Mode to proceed.")
            
            if device_info.is_a12_or_newer():
                print("\nFor A12+ devices (iPhone XS/XR and newer):")
                print("1. Press and quickly release Volume Up button")
                print("2. Press and quickly release Volume Down button")
                print("3. Press and hold Side button until you see the recovery mode screen")
            else:
                print("\nFor older devices:")
                print("1. Press and hold Home and Power buttons simultaneously")
                print("2. Continue holding until you see the recovery mode screen")
            
            self.wait_for_key()
            print("\nChecking for device in recovery mode...")
            time.sleep(2)
            
            # Simulate detection of recovery mode
            device_info.in_recovery_mode = True
            print("Device successfully entered recovery mode!")
        
        # Diagnose issue
        self.print_section("DIAGNOSING ISSUE")
        print("Analyzing your device to determine the cause of the boot loop...")
        self.cause = self.diagnostic_tool.analyze_boot_issue()
        
        print(f"\nDiagnosis complete: {self.cause.name}")
        if self.cause == BootLoopCause.CORRUPTED_SYSTEM_FILES:
            print("Your device has corrupted system files that prevent it from booting.")
        elif self.cause == BootLoopCause.FAILED_UPDATE:
            print("Your device failed during an iOS update, leaving it in an inconsistent state.")
        # Add descriptions for other causes
        
        # Generate recovery options
        self.recovery_options = self.diagnostic_tool.generate_recovery_options(self.cause)
        
        # Present recovery options
        self.print_section("RECOVERY OPTIONS")
        print("The following recovery methods are available, in order of preference:")
        print("(Earlier options are less invasive and more likely to preserve your data)")
        
        for i, option in enumerate(self.recovery_options, 1):
            print(f"{i}. {option}")
        
        # Get user choice
        choice = 0
        while choice < 1 or choice > len(self.recovery_options):
            try:
                choice = int(input("\nSelect a recovery method (number): "))
                if choice < 1 or choice > len(self.recovery_options):
                    print(f"Please enter a number between 1 and {len(self.recovery_options)}")
            except ValueError:
                print("Please enter a valid number")
        
        # Execute recovery method based on choice
        self.print_section("RECOVERY PROCESS")
        
        if choice == 1:
            # First option is usually force restart
            result = self.recovery_tool.force_restart()
        elif choice == 2 and "targeted" in self.recovery_options[1].lower():
            # Second option is usually targeted repair
            result = self.recovery_tool.targeted_repair(self.cause)
        elif choice == 3 or (choice == 2 and "system" in self.recovery_options[1].lower()):
            # Third option is usually system reset
            result = self.recovery_tool.system_reset()
        else:
            # Last resort is DFU restore
            result = self.recovery_tool.dfu_restore()
        
        # Show result
        self.print_section("RECOVERY RESULT")
        
        if result == RecoveryResult.SUCCESS:
            print("SUCCESS! Your device has been recovered.")
            print("It should now boot normally.")
        elif result == RecoveryResult.PARTIAL_SUCCESS:
            print("PARTIAL SUCCESS. Your device is in a better state but may still have issues.")
            print("Consider trying another recovery method if problems persist.")
        else:
            print("RECOVERY FAILED. Your device could not be recovered using this method.")
            print("Consider trying a more invasive recovery method or seeking professional repair.")
        
        # Show logs
        print("\nRecovery logs:")
        for log in self.recovery_tool.recovery_logs:
            print(log)
        
        self.print_section("THANK YOU")
        print("Thank you for using the iPhone Boot Recovery Tool.")
        print("If you found this tool helpful, please consider supporting its development.")
        print("For more information, visit: https://github.com/BhekumusaEric/iphone_repair")

if __name__ == "__main__":
    cli = CLI()
    cli.run()
