#!/usr/bin/env python3
"""
gui.py - Graphical User Interface for iPhone Boot Recovery Tool

This module provides a PyQt-based graphical interface for the recovery tool,
allowing users to diagnose and recover iPhones from boot loops with a
user-friendly interface.
"""

import os
import sys
import time
import logging
from typing import List, Optional, Dict, Any
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import PyQt5
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QComboBox, QTextEdit, QProgressBar,
        QMessageBox, QFrame, QSplitter, QTabWidget, QGroupBox,
        QRadioButton, QButtonGroup, QFileDialog, QDialog, QWizard,
        QWizardPage, QCheckBox, QListWidget, QListWidgetItem
    )
    from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QColor
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
    PYQT_AVAILABLE = True
except ImportError:
    logger.warning("PyQt5 not available, GUI will not be functional")
    PYQT_AVAILABLE = False

    # Create dummy classes to avoid errors
    class QMainWindow:
        pass

    class QThread:
        pass

    class pyqtSignal:
        def __init__(self, *args):
            pass

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.DiagnosticTool import DiagnosticTool, BootLoopCause, DeviceInfo
from core.RecoveryTool import RecoveryTool, RecoveryMethod, RecoveryResult
from core.UltimateRecovery import UltimateRecovery, UltimateRecoveryResult
from core.InheritanceSupport import InheritanceSupport, InheritanceSupportResult
from utils.device_communication import DeviceCommunication, DeviceMode

class WorkerThread(QThread):
    """Worker thread for background tasks"""

    # Define signals
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    task_complete = pyqtSignal(dict)
    task_error = pyqtSignal(str)

    def __init__(self, task_type, params=None):
        """
        Initialize worker thread

        Args:
            task_type: Type of task to perform
            params: Parameters for the task
        """
        super().__init__()
        self.task_type = task_type
        self.params = params or {}
        self.running = True

    def run(self):
        """Run the worker thread"""
        try:
            if self.task_type == "detect_device":
                self._detect_device()
            elif self.task_type == "diagnose_issue":
                self._diagnose_issue()
            elif self.task_type == "perform_recovery":
                self._perform_recovery()
            elif self.task_type == "perform_ultimate_recovery":
                self._perform_ultimate_recovery()
            elif self.task_type == "generate_inheritance_documents":
                self._generate_inheritance_documents()
            elif self.task_type == "generate_limited_documentation":
                self._generate_limited_documentation()
            else:
                self.task_error.emit(f"Unknown task type: {self.task_type}")
        except Exception as e:
            logger.error(f"Error in worker thread: {e}")
            self.task_error.emit(str(e))

    def _detect_device(self):
        """Detect connected iOS devices"""
        self.update_status.emit("Detecting connected devices...")
        self.update_progress.emit(10)

        # Create device communication instance
        comm = DeviceCommunication(simulate=self.params.get("simulate", True))

        # Detect devices
        self.update_progress.emit(30)
        devices = comm.detect_devices()

        self.update_progress.emit(70)

        if not devices:
            self.task_error.emit("No iOS devices detected")
            return

        # Get first device
        device = devices[0]

        # Create device info
        device_info = DeviceInfo()
        device_info.model = device.get("model", "Unknown")
        device_info.chip = device.get("chip_id", "A12 Bionic")  # Default to A12 if unknown
        device_info.ios_version = device.get("firmware_version", "Unknown")
        device_info.in_recovery_mode = device.get("mode") == DeviceMode.RECOVERY.name
        device_info.in_dfu_mode = device.get("mode") == DeviceMode.DFU.name

        self.update_progress.emit(100)
        self.update_status.emit(f"Detected: {device_info.model}")

        # Return device info
        self.task_complete.emit({
            "device_info": device_info,
            "raw_device": device
        })

    def _diagnose_issue(self):
        """Diagnose the cause of the boot loop"""
        device_info = self.params.get("device_info")

        if not device_info:
            self.task_error.emit("No device information provided")
            return

        self.update_status.emit("Analyzing boot issue...")
        self.update_progress.emit(20)

        # Create diagnostic tool
        diagnostic = DiagnosticTool()
        diagnostic.device_info = device_info

        # Analyze boot issue
        self.update_progress.emit(50)
        cause = diagnostic.analyze_boot_issue()

        # Generate recovery options
        self.update_progress.emit(80)
        options = diagnostic.generate_recovery_options(cause)

        self.update_progress.emit(100)
        self.update_status.emit(f"Diagnosis complete: {cause.name}")

        # Return diagnosis results
        self.task_complete.emit({
            "cause": cause,
            "options": options
        })

    def _perform_recovery(self):
        """Perform recovery based on selected method"""
        device_info = self.params.get("device_info")
        cause = self.params.get("cause")
        method = self.params.get("method")

        if not device_info or not cause or not method:
            self.task_error.emit("Missing required parameters")
            return

        self.update_status.emit(f"Starting recovery using {method}...")
        self.update_progress.emit(10)

        # Create recovery tool
        recovery = RecoveryTool(device_info)

        # Perform recovery based on method
        result = None

        if method == "force_restart":
            self.update_status.emit("Attempting force restart...")
            self.update_progress.emit(30)
            result = recovery.force_restart()
        elif method == "targeted_repair":
            self.update_status.emit("Attempting targeted system file repair...")
            self.update_progress.emit(30)
            result = recovery.targeted_repair(cause)
        elif method == "system_reset":
            self.update_status.emit("Performing system partition reset...")
            self.update_progress.emit(30)
            result = recovery.system_reset()
        elif method == "dfu_restore":
            self.update_status.emit("Performing DFU restore...")
            self.update_progress.emit(30)
            result = recovery.dfu_restore()
        else:
            self.task_error.emit(f"Unknown recovery method: {method}")
            return

        self.update_progress.emit(100)

        # Return recovery results
        self.task_complete.emit({
            "result": result,
            "logs": recovery.recovery_logs
        })

    def _perform_ultimate_recovery(self):
        """Perform ultimate recovery (last resort)"""
        device_info = self.params.get("device_info")

        if not device_info:
            self.task_error.emit("Missing device information")
            return

        self.update_status.emit("Starting ULTIMATE RECOVERY - this is a last resort method")
        self.update_progress.emit(10)

        # Create ultimate recovery tool
        recovery = UltimateRecovery(device_info, debug=True)

        # Check if device is in DFU mode
        if not device_info.in_dfu_mode:
            self.update_status.emit("Device must be in DFU mode for ultimate recovery")
            self.task_error.emit("Device must be in DFU mode for ultimate recovery. Please put your device in DFU mode and try again.")
            return

        # Perform ultimate recovery
        self.update_status.emit("Attempting aggressive recovery methods...")
        self.update_progress.emit(20)

        # Show progress updates for each step
        for i in range(20, 90, 10):
            self.update_progress.emit(i)
            time.sleep(1)  # Simulate progress

        # Perform the actual recovery
        result = recovery.perform_ultimate_recovery()

        self.update_progress.emit(100)

        # Return recovery results
        self.task_complete.emit({
            "result": result,
            "logs": recovery.logs,
            "ultimate": True
        })

    def _generate_inheritance_documents(self):
        """Generate inheritance documentation templates"""
        output_dir = self.params.get("output_dir")

        self.update_status.emit("Generating inheritance documentation templates...")
        self.update_progress.emit(10)

        # Create inheritance support tool
        support = InheritanceSupport(debug=True)

        # Provide guidance
        self.update_status.emit("Providing inheritance guidance...")
        self.update_progress.emit(30)
        support.provide_inheritance_guidance()

        # Generate documentation templates
        self.update_status.emit("Generating documentation templates...")
        self.update_progress.emit(50)
        templates = support.generate_documentation_templates(output_dir)

        # Get Apple support contact information
        self.update_status.emit("Getting Apple support contact information...")
        self.update_progress.emit(80)
        contact_info = support.provide_apple_support_contact_info()

        self.update_progress.emit(100)

        # Return results
        self.task_complete.emit({
            "templates": templates,
            "contact_info": contact_info,
            "logs": support.logs,
            "inheritance": True
        })

    def _generate_limited_documentation(self):
        """Generate limited documentation templates"""
        output_dir = self.params.get("output_dir")

        self.update_status.emit("Generating limited documentation templates...")
        self.update_progress.emit(10)

        # Create inheritance support tool
        support = InheritanceSupport(debug=True)

        # Provide guidance for limited documentation
        self.update_status.emit("Providing guidance for limited documentation cases...")
        self.update_progress.emit(30)
        support.provide_limited_documentation_guidance()

        # Generate limited documentation templates
        self.update_status.emit("Generating alternative documentation templates...")
        self.update_progress.emit(50)
        templates = support.generate_limited_documentation_templates(output_dir)

        # Get Apple support contact information
        self.update_status.emit("Getting Apple support contact information...")
        self.update_progress.emit(80)
        contact_info = support.provide_apple_support_contact_info()

        self.update_progress.emit(100)

        # Return results
        self.task_complete.emit({
            "templates": templates,
            "contact_info": contact_info,
            "logs": support.logs,
            "limited_documentation": True
        })

class MainWindow(QMainWindow):
    """Main window for the iPhone Boot Recovery Tool GUI"""

    def __init__(self):
        """Initialize the main window"""
        super().__init__()

        # Initialize variables
        self.device_info = None
        self.diagnosis_cause = None
        self.recovery_options = []
        self.worker_thread = None

        # Set up the UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle("iPhone Boot Recovery Tool")
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)

        # Create header
        header_label = QLabel("iPhone Boot Recovery Tool")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(header_label)

        subtitle_label = QLabel("A12+ Device Recovery Specialist")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 16px; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_device_tab()
        self.create_diagnosis_tab()
        self.create_recovery_tab()
        self.create_inheritance_tab()
        self.create_logs_tab()

        # Create status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Disable tabs initially
        self.tab_widget.setTabEnabled(1, False)  # Diagnosis tab
        self.tab_widget.setTabEnabled(2, False)  # Recovery tab

        # Show the window
        self.show()

    def create_device_tab(self):
        """Create the device detection tab"""
        device_tab = QWidget()
        layout = QVBoxLayout(device_tab)

        # Create device detection group
        device_group = QGroupBox("Device Detection")
        device_layout = QVBoxLayout(device_group)

        # Add instructions
        instructions_label = QLabel(
            "Connect your iPhone to this computer using a Lightning or USB-C cable.\n"
            "If your device is not already in recovery mode, the tool will guide you."
        )
        instructions_label.setWordWrap(True)
        device_layout.addWidget(instructions_label)

        # Add detect button
        detect_button = QPushButton("Detect Device")
        detect_button.clicked.connect(self.detect_device)
        device_layout.addWidget(detect_button)

        # Add simulation checkbox
        self.simulate_checkbox = QCheckBox("Simulation Mode (for testing)")
        self.simulate_checkbox.setChecked(True)
        device_layout.addWidget(self.simulate_checkbox)

        # Add device info display
        self.device_info_text = QTextEdit()
        self.device_info_text.setReadOnly(True)
        self.device_info_text.setMinimumHeight(200)
        device_layout.addWidget(self.device_info_text)

        # Add to layout
        layout.addWidget(device_group)

        # Add recovery mode guide
        recovery_group = QGroupBox("Recovery Mode Guide")
        recovery_layout = QVBoxLayout(recovery_group)

        recovery_label = QLabel(
            "<b>For A12+ devices (iPhone XS/XR and newer):</b><br>"
            "1. Press and quickly release Volume Up button<br>"
            "2. Press and quickly release Volume Down button<br>"
            "3. Press and hold Side button until you see the recovery mode screen<br><br>"
            "<b>For older devices:</b><br>"
            "1. Press and hold Home and Power buttons simultaneously<br>"
            "2. Continue holding until you see the recovery mode screen"
        )
        recovery_label.setWordWrap(True)
        recovery_layout.addWidget(recovery_label)

        # Add to layout
        layout.addWidget(recovery_group)

        # Add spacer
        layout.addStretch()

        # Add to tab widget
        self.tab_widget.addTab(device_tab, "Device Detection")

    def create_diagnosis_tab(self):
        """Create the diagnosis tab"""
        diagnosis_tab = QWidget()
        layout = QVBoxLayout(diagnosis_tab)

        # Create diagnosis group
        diagnosis_group = QGroupBox("Boot Issue Diagnosis")
        diagnosis_layout = QVBoxLayout(diagnosis_group)

        # Add instructions
        instructions_label = QLabel(
            "Click the button below to analyze your device and determine the cause of the boot loop."
        )
        instructions_label.setWordWrap(True)
        diagnosis_layout.addWidget(instructions_label)

        # Add diagnose button
        diagnose_button = QPushButton("Diagnose Boot Issue")
        diagnose_button.clicked.connect(self.diagnose_issue)
        diagnosis_layout.addWidget(diagnose_button)

        # Add diagnosis result display
        self.diagnosis_text = QTextEdit()
        self.diagnosis_text.setReadOnly(True)
        self.diagnosis_text.setMinimumHeight(200)
        diagnosis_layout.addWidget(self.diagnosis_text)

        # Add to layout
        layout.addWidget(diagnosis_group)

        # Add spacer
        layout.addStretch()

        # Add to tab widget
        self.tab_widget.addTab(diagnosis_tab, "Diagnosis")

    def create_recovery_tab(self):
        """Create the recovery tab"""
        recovery_tab = QWidget()
        layout = QVBoxLayout(recovery_tab)

        # Create recovery options group
        options_group = QGroupBox("Recovery Options")
        options_layout = QVBoxLayout(options_group)

        # Add instructions
        instructions_label = QLabel(
            "Select a recovery method from the list below. Earlier options are less invasive "
            "and more likely to preserve your data."
        )
        instructions_label.setWordWrap(True)
        options_layout.addWidget(instructions_label)

        # Add options list
        self.options_list = QListWidget()
        self.options_list.setMinimumHeight(150)
        options_layout.addWidget(self.options_list)

        # Add recover button
        recover_button = QPushButton("Start Recovery")
        recover_button.clicked.connect(self.perform_recovery)
        options_layout.addWidget(recover_button)

        # Add to layout
        layout.addWidget(options_group)

        # Create recovery status group
        status_group = QGroupBox("Recovery Status")
        status_layout = QVBoxLayout(status_group)

        # Add status display
        self.recovery_status_text = QTextEdit()
        self.recovery_status_text.setReadOnly(True)
        self.recovery_status_text.setMinimumHeight(200)
        status_layout.addWidget(self.recovery_status_text)

        # Add to layout
        layout.addWidget(status_group)

        # Create ultimate recovery group
        ultimate_group = QGroupBox("ULTIMATE RECOVERY - LAST RESORT")
        ultimate_layout = QVBoxLayout(ultimate_group)

        # Add warning label
        warning_label = QLabel(
            "<b>WARNING: ULTIMATE RECOVERY IS A LAST RESORT METHOD</b><br><br>"
            "This method attempts aggressive recovery techniques that prioritize "
            "device access over data preservation and security. It should only be "
            "used when all other methods have failed and you are willing to:<br><br>"
            "• Potentially lose ALL data on the device<br>"
            "• Bypass security measures<br>"
            "• Possibly void your warranty<br>"
            "• Accept that success is not guaranteed<br><br>"
            "Your device must be in DFU mode to use this method."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: red;")
        ultimate_layout.addWidget(warning_label)

        # Add ultimate recovery button
        ultimate_button = QPushButton("I UNDERSTAND THE RISKS - PERFORM ULTIMATE RECOVERY")
        ultimate_button.setStyleSheet("background-color: #FF4500; color: white; font-weight: bold; padding: 10px;")
        ultimate_button.clicked.connect(self.perform_ultimate_recovery)
        ultimate_layout.addWidget(ultimate_button)

        # Add to layout
        layout.addWidget(ultimate_group)

        # Add to tab widget
        self.tab_widget.addTab(recovery_tab, "Recovery")

    def create_inheritance_tab(self):
        """Create the inheritance support tab"""
        inheritance_tab = QWidget()
        layout = QVBoxLayout(inheritance_tab)

        # Create inheritance support group
        support_group = QGroupBox("Inherited Device Support")
        support_layout = QVBoxLayout(support_group)

        # Add explanation
        explanation_label = QLabel(
            "<b>Inherited Device Support</b><br><br>"
            "This feature provides guidance and documentation for users who have inherited "
            "devices but cannot access them due to activation lock or unknown credentials.<br><br>"
            "If you have inherited an iPhone from someone who has passed away and cannot "
            "access it due to iCloud Activation Lock or unknown credentials, Apple has an "
            "official process to help with legitimate inheritance cases.<br><br>"
            "<b>Note:</b> This requires proper documentation to prove legitimate inheritance."
        )
        explanation_label.setWordWrap(True)
        support_layout.addWidget(explanation_label)

        # Add generate documentation button
        docs_button = QPushButton("Generate Documentation Templates")
        docs_button.clicked.connect(self.generate_inheritance_documents)
        support_layout.addWidget(docs_button)

        # Add contact Apple button
        contact_button = QPushButton("Show Apple Support Contact Information")
        contact_button.clicked.connect(self.show_apple_support_info)
        support_layout.addWidget(contact_button)

        # Add to layout
        layout.addWidget(support_group)

        # Create documentation group
        docs_group = QGroupBox("Required Documentation")
        docs_layout = QVBoxLayout(docs_group)

        # Add documentation info
        docs_label = QLabel(
            "<b>Documentation typically required by Apple:</b><br><br>"
            "1. <b>Death Certificate</b> - Original or certified copy<br>"
            "2. <b>Proof of Inheritance</b> - Will, probate document, or court order<br>"
            "3. <b>Your Government-issued ID</b> - To verify your identity<br>"
            "4. <b>Proof of Relationship</b> - Documents showing your relationship to the deceased<br>"
            "5. <b>Proof of Purchase</b> (if available) - Original receipt or other proof<br><br>"
            "The documentation templates will help you prepare these documents in the format "
            "Apple typically requires for inherited device requests."
        )
        docs_label.setWordWrap(True)
        docs_layout.addWidget(docs_label)

        # Add to layout
        layout.addWidget(docs_group)

        # Create limited documentation group
        limited_docs_group = QGroupBox("Limited Documentation Support")
        limited_docs_layout = QVBoxLayout(limited_docs_group)

        # Add limited documentation info
        limited_docs_label = QLabel(
            "<b>Don't have all the standard documentation?</b><br><br>"
            "If you cannot provide all the standard documentation (like in cases where you only have "
            "an affidavit or limited proof), we can help with alternative approaches:<br><br>"
            "• Affidavit templates for sworn statements<br>"
            "• Third-party verification forms<br>"
            "• Guides for gathering circumstantial evidence<br>"
            "• Legal aid resources<br>"
            "• Alternative options when recovery isn't possible<br><br>"
            "While these alternatives don't guarantee success with Apple, they can help build "
            "the strongest possible case with the documentation you have available."
        )
        limited_docs_label.setWordWrap(True)
        limited_docs_layout.addWidget(limited_docs_label)

        # Add limited documentation button
        limited_docs_button = QPushButton("Generate Limited Documentation Templates")
        limited_docs_button.clicked.connect(self.generate_limited_documentation)
        limited_docs_layout.addWidget(limited_docs_button)

        # Add to layout
        layout.addWidget(limited_docs_group)

        # Create legal notice group
        legal_group = QGroupBox("Legal Notice")
        legal_layout = QVBoxLayout(legal_group)

        # Add legal notice
        legal_label = QLabel(
            "<b>Important Legal Notice:</b><br><br>"
            "This tool provides guidance for legitimate inheritance cases only. It does NOT "
            "attempt to bypass security measures or activation locks.<br><br>"
            "Attempting to bypass activation lock through unofficial means may violate laws "
            "including the Digital Millennium Copyright Act (DMCA) and Computer Fraud and "
            "Abuse Act (CFAA), as well as Apple's Terms of Service.<br><br>"
            "Always follow Apple's official process for inherited devices."
        )
        legal_label.setWordWrap(True)
        legal_label.setStyleSheet("color: #CC0000;")
        legal_layout.addWidget(legal_label)

        # Add to layout
        layout.addWidget(legal_group)

        # Add to tab widget
        self.tab_widget.addTab(inheritance_tab, "Inherited Device")

    def create_logs_tab(self):
        """Create the logs tab"""
        logs_tab = QWidget()
        layout = QVBoxLayout(logs_tab)

        # Create logs group
        logs_group = QGroupBox("Recovery Logs")
        logs_layout = QVBoxLayout(logs_group)

        # Add logs display
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMinimumHeight(400)
        logs_layout.addWidget(self.logs_text)

        # Add save logs button
        save_button = QPushButton("Save Logs")
        save_button.clicked.connect(self.save_logs)
        logs_layout.addWidget(save_button)

        # Add to layout
        layout.addWidget(logs_group)

        # Add to tab widget
        self.tab_widget.addTab(logs_tab, "Logs")

    def detect_device(self):
        """Detect connected iOS devices"""
        # Clear previous device info
        self.device_info_text.clear()
        self.device_info = None

        # Disable tabs
        self.tab_widget.setTabEnabled(1, False)  # Diagnosis tab
        self.tab_widget.setTabEnabled(2, False)  # Recovery tab

        # Create worker thread
        self.worker_thread = WorkerThread(
            "detect_device",
            {"simulate": self.simulate_checkbox.isChecked()}
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.device_detected)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def device_detected(self, result):
        """Handle device detection results"""
        # Store device info
        self.device_info = result["device_info"]
        raw_device = result["raw_device"]

        # Display device info
        self.device_info_text.clear()
        self.device_info_text.append(f"<b>Detected device:</b> {self.device_info.model}")
        self.device_info_text.append(f"<b>Chip:</b> {self.device_info.chip}")
        self.device_info_text.append(f"<b>iOS Version:</b> {self.device_info.ios_version}")
        self.device_info_text.append(f"<b>Recovery Mode:</b> {'Yes' if self.device_info.in_recovery_mode else 'No'}")
        self.device_info_text.append(f"<b>DFU Mode:</b> {'Yes' if self.device_info.in_dfu_mode else 'No'}")

        # Add raw device info
        self.device_info_text.append("\n<b>Raw Device Information:</b>")
        for key, value in raw_device.items():
            if key not in ["udid", "name", "model", "firmware_version", "mode"]:
                self.device_info_text.append(f"<b>{key}:</b> {value}")

        # Enable diagnosis tab
        self.tab_widget.setTabEnabled(1, True)

        # Switch to diagnosis tab
        self.tab_widget.setCurrentIndex(1)

    def diagnose_issue(self):
        """Diagnose the cause of the boot loop"""
        # Clear previous diagnosis
        self.diagnosis_text.clear()
        self.diagnosis_cause = None
        self.recovery_options = []

        # Disable recovery tab
        self.tab_widget.setTabEnabled(2, False)

        # Create worker thread
        self.worker_thread = WorkerThread(
            "diagnose_issue",
            {"device_info": self.device_info}
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.issue_diagnosed)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def issue_diagnosed(self, result):
        """Handle diagnosis results"""
        # Store diagnosis results
        self.diagnosis_cause = result["cause"]
        self.recovery_options = result["options"]

        # Display diagnosis results
        self.diagnosis_text.clear()
        self.diagnosis_text.append(f"<b>Diagnosis complete:</b> {self.diagnosis_cause.name}")

        # Add description based on cause
        if self.diagnosis_cause == BootLoopCause.CORRUPTED_SYSTEM_FILES:
            self.diagnosis_text.append("\nYour device has corrupted system files that prevent it from booting.")
        elif self.diagnosis_cause == BootLoopCause.FAILED_UPDATE:
            self.diagnosis_text.append("\nYour device failed during an iOS update, leaving it in an inconsistent state.")
        elif self.diagnosis_cause == BootLoopCause.HARDWARE_FAILURE:
            self.diagnosis_text.append("\nYour device may have a hardware issue that prevents it from booting.")
        elif self.diagnosis_cause == BootLoopCause.JAILBREAK_ISSUE:
            self.diagnosis_text.append("\nYour device has issues related to a jailbreak attempt or tweak.")
        elif self.diagnosis_cause == BootLoopCause.THIRD_PARTY_APP:
            self.diagnosis_text.append("\nA third-party app is causing your device to fail during boot.")
        elif self.diagnosis_cause == BootLoopCause.LOW_LEVEL_BOOTLOADER:
            self.diagnosis_text.append("\nYour device has a low-level bootloader issue.")
        else:
            self.diagnosis_text.append("\nThe cause of the boot loop could not be determined.")

        # Display recovery options
        self.diagnosis_text.append("\n<b>Recovery Options:</b>")
        for i, option in enumerate(self.recovery_options, 1):
            self.diagnosis_text.append(f"{i}. {option}")

        # Update recovery options list
        self.options_list.clear()
        for option in self.recovery_options:
            self.options_list.addItem(option)

        # Select first option
        if self.options_list.count() > 0:
            self.options_list.setCurrentRow(0)

        # Enable recovery tab
        self.tab_widget.setTabEnabled(2, True)

        # Switch to recovery tab
        self.tab_widget.setCurrentIndex(2)

    def perform_recovery(self):
        """Perform recovery based on selected method"""
        # Get selected option
        selected_items = self.options_list.selectedItems()
        if not selected_items:
            self.show_error("Please select a recovery method")
            return

        selected_option = selected_items[0].text()
        selected_index = self.options_list.currentRow()

        # Determine recovery method
        method = None
        if selected_index == 0:
            method = "force_restart"
        elif "targeted" in selected_option.lower():
            method = "targeted_repair"
        elif "system" in selected_option.lower():
            method = "system_reset"
        elif "restore" in selected_option.lower():
            method = "dfu_restore"

        if not method:
            self.show_error("Unknown recovery method")
            return

        # Confirm DFU restore if selected
        if method == "dfu_restore":
            reply = QMessageBox.warning(
                self,
                "Data Loss Warning",
                "DFU restore will erase all data on your device. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.No:
                return

        # Clear previous recovery status
        self.recovery_status_text.clear()

        # Create worker thread
        self.worker_thread = WorkerThread(
            "perform_recovery",
            {
                "device_info": self.device_info,
                "cause": self.diagnosis_cause,
                "method": method
            }
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.recovery_completed)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def recovery_completed(self, result):
        """Handle recovery results"""
        # Get results
        recovery_result = result["result"]
        logs = result["logs"]
        is_ultimate = result.get("ultimate", False)

        # Display recovery status
        self.recovery_status_text.clear()

        if is_ultimate:
            # Handle ultimate recovery result
            if recovery_result == UltimateRecoveryResult.SUCCESS:
                self.recovery_status_text.append("<b>ULTIMATE RECOVERY SUCCESSFUL!</b> Your device has been recovered.")
                self.recovery_status_text.append("It should now boot with bypassed restrictions.")
                self.recovery_status_text.append("<b>WARNING:</b> Your device may be in an insecure state and all data may have been compromised.")
            elif recovery_result == UltimateRecoveryResult.PARTIAL_SUCCESS:
                self.recovery_status_text.append("<b>PARTIAL SUCCESS.</b> Your device is in a better state but may still have issues.")
                self.recovery_status_text.append("Some restrictions may have been bypassed.")
            else:
                self.recovery_status_text.append("<b>ULTIMATE RECOVERY FAILED.</b> Your device could not be recovered using aggressive methods.")
                self.recovery_status_text.append("Consider seeking professional repair services.")
        else:
            # Handle normal recovery result
            if recovery_result == RecoveryResult.SUCCESS:
                self.recovery_status_text.append("<b>SUCCESS!</b> Your device has been recovered.")
                self.recovery_status_text.append("It should now boot normally.")
            elif recovery_result == RecoveryResult.PARTIAL_SUCCESS:
                self.recovery_status_text.append("<b>PARTIAL SUCCESS.</b> Your device is in a better state but may still have issues.")
                self.recovery_status_text.append("Consider trying another recovery method if problems persist.")
            else:
                self.recovery_status_text.append("<b>RECOVERY FAILED.</b> Your device could not be recovered using this method.")
                self.recovery_status_text.append("Consider trying a more invasive recovery method or seeking professional repair.")

        # Display logs
        self.logs_text.clear()
        self.logs_text.append("<b>Recovery Logs:</b>")
        for log in logs:
            self.logs_text.append(log)

        # Switch to logs tab
        self.tab_widget.setCurrentIndex(3)

    def perform_ultimate_recovery(self):
        """Perform ultimate recovery (last resort)"""
        # Confirm ultimate recovery
        reply = QMessageBox.warning(
            self,
            "ULTIMATE RECOVERY - FINAL WARNING",
            "You are about to perform ULTIMATE RECOVERY, which:\n\n"
            "• May PERMANENTLY ERASE ALL DATA on your device\n"
            "• Will attempt to BYPASS SECURITY MEASURES\n"
            "• Could potentially VOID YOUR WARRANTY\n"
            "• May leave your device in an INSECURE STATE\n\n"
            "This is truly a LAST RESORT method when all else has failed.\n\n"
            "Are you ABSOLUTELY SURE you want to proceed?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # Check if device is in DFU mode
        if not self.device_info or not self.device_info.in_dfu_mode:
            self.show_error(
                "Your device must be in DFU mode for ultimate recovery.\n\n"
                "Please put your device in DFU mode and try again.\n\n"
                "For A12+ devices (iPhone XS/XR and newer):\n"
                "1. Connect device to computer\n"
                "2. Press and quickly release Volume Up button\n"
                "3. Press and quickly release Volume Down button\n"
                "4. Press and hold Side button until screen goes black\n"
                "5. While continuing to hold Side button, press and hold Volume Down button for 5 seconds\n"
                "6. Release Side button while continuing to hold Volume Down button for another 5 seconds"
            )
            return

        # Clear previous recovery status
        self.recovery_status_text.clear()
        self.recovery_status_text.append("<b>STARTING ULTIMATE RECOVERY...</b>")
        self.recovery_status_text.append("This process may take several minutes. Please do not disconnect your device.")
        self.recovery_status_text.append("Your device screen may display various images or remain black during this process.")

        # Create worker thread
        self.worker_thread = WorkerThread(
            "perform_ultimate_recovery",
            {"device_info": self.device_info}
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.recovery_completed)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def save_logs(self):
        """Save logs to a file"""
        # Get logs text
        logs = self.logs_text.toPlainText()

        if not logs:
            self.show_error("No logs to save")
            return

        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Logs",
            os.path.expanduser("~/recovery_logs.txt"),
            "Text Files (*.txt)"
        )

        if not file_path:
            return

        # Save logs
        try:
            with open(file_path, "w") as f:
                f.write(logs)

            self.update_status(f"Logs saved to {file_path}")
        except Exception as e:
            self.show_error(f"Error saving logs: {e}")

    def update_status(self, status):
        """Update status bar message"""
        self.status_bar.showMessage(status)

    def update_progress(self, value):
        """Update progress bar value"""
        self.progress_bar.setValue(value)

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.update_status("Error: " + message)
        self.progress_bar.setValue(0)

    def generate_inheritance_documents(self):
        """Generate inheritance documentation templates"""
        # Get output directory
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory for Documentation Templates",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )

        if not output_dir:
            return

        # Create worker thread
        self.worker_thread = WorkerThread(
            "generate_inheritance_documents",
            {"output_dir": output_dir}
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.inheritance_documents_generated)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def inheritance_documents_generated(self, result):
        """Handle inheritance documents generation results"""
        # Get results
        templates = result["templates"]
        contact_info = result["contact_info"]
        logs = result["logs"]

        # Display success message
        message = (
            f"Documentation templates have been generated in:\n\n"
            f"{os.path.dirname(list(templates.values())[0])}\n\n"
            f"The following templates were created:\n"
        )

        for name, path in templates.items():
            message += f"• {name}: {os.path.basename(path)}\n"

        message += (
            f"\nPlease fill out these templates with your information and follow "
            f"Apple's official process for inherited devices."
        )

        QMessageBox.information(
            self,
            "Documentation Templates Generated",
            message
        )

        # Display logs
        self.logs_text.clear()
        self.logs_text.append("<b>Inheritance Support Logs:</b>")
        for log in logs:
            self.logs_text.append(log)

        # Switch to logs tab
        self.tab_widget.setCurrentIndex(4)  # Logs tab

    def show_apple_support_info(self):
        """Show Apple support contact information"""
        # Create inheritance support
        support = InheritanceSupport()

        # Get contact information
        contact_info = support.provide_apple_support_contact_info()

        # Display contact information
        message = (
            f"<b>Apple Support Contact Information:</b><br><br>"
            f"<b>Website:</b> <a href='{contact_info['website']}'>{contact_info['website']}</a><br>"
            f"<b>Phone (US):</b> {contact_info['phone_us']}<br>"
            f"<b>Inheritance Information:</b> <a href='{contact_info['inheritance_info']}'>{contact_info['inheritance_info']}</a><br>"
            f"<b>Find an Apple Store:</b> <a href='{contact_info['apple_store']}'>{contact_info['apple_store']}</a><br>"
            f"<b>Online Chat:</b> <a href='{contact_info['online_chat']}'>{contact_info['online_chat']}</a><br><br>"
            f"<b>Next Steps:</b><br>"
            f"1. Gather all required documentation<br>"
            f"2. Contact Apple Support using one of the methods above<br>"
            f"3. Explain that you have inherited a device and need assistance with activation lock<br>"
            f"4. Follow their specific instructions for your case"
        )

        # Create message box with clickable links
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Apple Support Contact Information")
        msg_box.setText(message)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def generate_limited_documentation(self):
        """Generate limited documentation templates"""
        # Get output directory
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory for Limited Documentation Templates",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )

        if not output_dir:
            return

        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Limited Documentation Confirmation",
            "This will generate templates for cases with limited documentation, such as:\n\n"
            "• Affidavit templates\n"
            "• Third-party verification forms\n"
            "• Guides for gathering circumstantial evidence\n"
            "• Legal aid resources\n"
            "• Alternative options when recovery isn't possible\n\n"
            "These templates are designed for cases where standard documentation is unavailable.\n\n"
            "Do you want to proceed?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.No:
            return

        # Create worker thread
        self.worker_thread = WorkerThread(
            "generate_limited_documentation",
            {"output_dir": output_dir}
        )

        # Connect signals
        self.worker_thread.update_status.connect(self.update_status)
        self.worker_thread.update_progress.connect(self.update_progress)
        self.worker_thread.task_complete.connect(self.limited_documentation_generated)
        self.worker_thread.task_error.connect(self.show_error)

        # Start thread
        self.worker_thread.start()

    def limited_documentation_generated(self, result):
        """Handle limited documentation generation results"""
        # Get results
        templates = result["templates"]
        contact_info = result["contact_info"]  # Not used but kept for consistency
        logs = result["logs"]

        # Display success message
        message = (
            f"Limited documentation templates have been generated in:\n\n"
            f"{os.path.dirname(list(templates.values())[0])}\n\n"
            f"The following templates were created:\n"
        )

        for name, path in templates.items():
            message += f"• {name}: {os.path.basename(path)}\n"

        message += (
            f"\nThese templates can help build a case with the limited documentation you have available. "
            f"While they don't guarantee success with Apple, they provide the best chance "
            f"for cases with non-standard documentation."
        )

        QMessageBox.information(
            self,
            "Limited Documentation Templates Generated",
            message
        )

        # Display logs
        self.logs_text.clear()
        self.logs_text.append("<b>Limited Documentation Support Logs:</b>")
        for log in logs:
            self.logs_text.append(log)

        # Switch to logs tab
        self.tab_widget.setCurrentIndex(4)  # Logs tab

def run_gui():
    """Run the GUI application"""
    if not PYQT_AVAILABLE:
        print("PyQt5 is not available. Please install it to use the GUI.")
        print("You can install it with: pip install PyQt5")
        return 1

    app = QApplication(sys.argv)
    window = MainWindow()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(run_gui())
