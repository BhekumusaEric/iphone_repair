"""
Core module for iPhone Boot Recovery Tool

This package contains the core functionality for diagnosing and recovering
iPhones stuck in boot loops, with special focus on A12 chip devices.
"""

from .DiagnosticTool import DiagnosticTool, BootLoopCause, DeviceInfo
from .RecoveryTool import RecoveryTool, RecoveryMethod, RecoveryResult
from .AdvancedRecovery import AdvancedRecovery, FilesystemRepairResult, FirmwarePatchResult

__all__ = [
    'DiagnosticTool',
    'BootLoopCause',
    'DeviceInfo',
    'RecoveryTool',
    'RecoveryMethod',
    'RecoveryResult',
    'AdvancedRecovery',
    'FilesystemRepairResult',
    'FirmwarePatchResult'
]
