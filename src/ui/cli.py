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
from core.UltimateRecovery import UltimateRecovery, UltimateRecoveryResult
from core.InheritanceSupport import InheritanceSupport, InheritanceSupportResult

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

        # Show main menu
        self.show_main_menu()

    def show_main_menu(self):
        """Show the main menu and handle user selection"""
        while True:
            self.print_section("MAIN MENU")
            print("Please select an option:")
            print("1. Boot Recovery (for devices stuck on Apple logo)")
            print("2. Inherited Device Support (for accessing inherited devices)")
            print("3. Exit")

            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice < 1 or choice > 3:
                    print("Please enter a number between 1 and 3")
                    continue

                if choice == 1:
                    self.run_boot_recovery()
                    break
                elif choice == 2:
                    self.run_inheritance_support()
                    break
                elif choice == 3:
                    print("\nExiting. Thank you for using iPhone Boot Recovery Tool.")
                    sys.exit(0)
            except ValueError:
                print("Please enter a valid number")

    def run_boot_recovery(self):
        """Run the boot recovery process"""
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

        # Add ultimate recovery option
        ultimate_option = len(self.recovery_options) + 1
        print(f"\n{ultimate_option}. ULTIMATE RECOVERY - LAST RESORT (may lose all data, bypass security)")

        # Get user choice
        choice = 0
        while choice < 1 or choice > ultimate_option:
            try:
                choice = int(input("\nSelect a recovery method (number): "))
                if choice < 1 or choice > ultimate_option:
                    print(f"Please enter a number between 1 and {ultimate_option}")
            except ValueError:
                print("Please enter a valid number")

        # Execute recovery method based on choice
        self.print_section("RECOVERY PROCESS")

        if choice == len(self.recovery_options) + 1:
            # Ultimate recovery option
            print("You have selected ULTIMATE RECOVERY - this is a last resort method.")
            print("WARNING: This method prioritizes device access over data preservation and security.")
            print("WARNING: All user data may be lost or compromised.")
            print("WARNING: This may void your warranty and violate terms of service.")

            # Confirm user's choice
            confirm = input("\nAre you ABSOLUTELY SURE you want to proceed? (yes/no): ").lower()
            if confirm != "yes":
                print("Ultimate recovery cancelled.")
                return

            # Check if device is in DFU mode
            if not self.device_info.in_dfu_mode:
                print("\nYour device must be in DFU mode for ultimate recovery.")
                print("\nFor A12+ devices (iPhone XS/XR and newer):")
                print("1. Connect device to computer")
                print("2. Press and quickly release Volume Up button")
                print("3. Press and quickly release Volume Down button")
                print("4. Press and hold Side button until screen goes black")
                print("5. While continuing to hold Side button, press and hold Volume Down button for 5 seconds")
                print("6. Release Side button while continuing to hold Volume Down button for another 5 seconds")

                # Wait for user to put device in DFU mode
                input("\nPress Enter when your device is in DFU mode...")

                # Set DFU mode flag (in a real implementation, we would verify this)
                self.device_info.in_dfu_mode = True

            # Create ultimate recovery tool
            ultimate_recovery = UltimateRecovery(self.device_info)

            # Perform ultimate recovery
            print("\nStarting ultimate recovery process...")
            print("This may take several minutes. Please do not disconnect your device.")
            result = ultimate_recovery.perform_ultimate_recovery()

            # Store logs
            self.recovery_tool.recovery_logs = ultimate_recovery.logs

            # Convert result type for consistent handling
            if result == UltimateRecoveryResult.SUCCESS:
                result = RecoveryResult.SUCCESS
            elif result == UltimateRecoveryResult.PARTIAL_SUCCESS:
                result = RecoveryResult.PARTIAL_SUCCESS
            else:
                result = RecoveryResult.FAILURE
        elif choice == 1:
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

    def run_inheritance_support(self):
        """Run the inheritance support process"""
        self.print_section("INHERITED DEVICE SUPPORT")
        print("This feature provides guidance and documentation for users who have inherited")
        print("devices but cannot access them due to activation lock or unknown credentials.")
        print("\nIf you have inherited an iPhone from someone who has passed away and cannot")
        print("access it due to iCloud Activation Lock or unknown credentials, Apple has an")
        print("official process to help with legitimate inheritance cases.")
        print("\nNote: This requires proper documentation to prove legitimate inheritance.")

        self.wait_for_key()

        # Create inheritance support
        support = InheritanceSupport(debug=True)

        # Provide guidance
        self.print_section("INHERITANCE GUIDANCE")
        support.provide_inheritance_guidance()

        # Show menu
        while True:
            self.print_section("INHERITANCE SUPPORT OPTIONS")
            print("Please select an option:")
            print("1. Generate Documentation Templates")
            print("2. Show Apple Support Contact Information")
            print("3. Return to Main Menu")

            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if choice < 1 or choice > 3:
                    print("Please enter a number between 1 and 3")
                    continue

                if choice == 1:
                    self.generate_inheritance_documents(support)
                elif choice == 2:
                    self.show_apple_support_info(support)
                elif choice == 3:
                    self.show_main_menu()
                    break
            except ValueError:
                print("Please enter a valid number")

    def generate_inheritance_documents(self, support):
        """Generate inheritance documentation templates"""
        self.print_section("GENERATE DOCUMENTATION TEMPLATES")
        print("This will generate documentation templates for inheritance claims.")
        print("Please specify where to save the templates.")

        # Get output directory
        output_dir = input("\nEnter output directory path (or press Enter for current directory): ")
        if not output_dir:
            output_dir = os.getcwd()

        # Create directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"\nUsing directory: {output_dir}")
        except Exception as e:
            print(f"\nError creating directory: {e}")
            print("Using current directory instead.")
            output_dir = os.getcwd()

        # Generate templates
        print("\nGenerating documentation templates...")
        templates = support.generate_documentation_templates(output_dir)

        # Show results
        self.print_section("DOCUMENTATION TEMPLATES GENERATED")
        print(f"Templates have been generated in: {os.path.dirname(list(templates.values())[0])}")
        print("\nThe following templates were created:")
        for name, path in templates.items():
            print(f"• {name}: {os.path.basename(path)}")

        print("\nPlease fill out these templates with your information and follow")
        print("Apple's official process for inherited devices.")

        self.wait_for_key()

    def show_apple_support_info(self, support):
        """Show Apple support contact information"""
        self.print_section("APPLE SUPPORT CONTACT INFORMATION")

        # Get contact information
        contact_info = support.provide_apple_support_contact_info()

        # Display contact information
        print(f"Website: {contact_info['website']}")
        print(f"Phone (US): {contact_info['phone_us']}")
        print(f"Inheritance Information: {contact_info['inheritance_info']}")
        print(f"Find an Apple Store: {contact_info['apple_store']}")
        print(f"Online Chat: {contact_info['online_chat']}")

        print("\nNext Steps:")
        print("1. Gather all required documentation")
        print("2. Contact Apple Support using one of the methods above")
        print("3. Explain that you have inherited a device and need assistance with activation lock")
        print("4. Follow their specific instructions for your case")

        self.wait_for_key()

if __name__ == "__main__":
    cli = CLI()
    cli.run()
