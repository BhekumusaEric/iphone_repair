"""
Utils module for iPhone Boot Recovery Tool

This package contains utility functions and classes for the recovery tool,
including device communication and filesystem operations.
"""

# Import device communication classes
from .device_communication import DeviceCommunication, DeviceMode, DeviceError, DeviceNotFoundError

# Try to import libimobiledevice wrapper
try:
    from .libimobile_wrapper import LibimobileWrapper
    LIBIMOBILEDEVICE_AVAILABLE = True
except ImportError:
    LIBIMOBILEDEVICE_AVAILABLE = False

__all__ = [
    'DeviceCommunication',
    'DeviceMode',
    'DeviceError',
    'DeviceNotFoundError',
    'LIBIMOBILEDEVICE_AVAILABLE'
]

if LIBIMOBILEDEVICE_AVAILABLE:
    __all__.append('LibimobileWrapper')
