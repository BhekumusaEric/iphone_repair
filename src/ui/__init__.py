"""
UI module for iPhone Boot Recovery Tool

This package contains user interface components for the recovery tool,
including command-line and graphical interfaces.
"""

from .cli import CLI

# Try to import GUI components
try:
    from .gui import MainWindow, run_gui, PYQT_AVAILABLE
except ImportError:
    PYQT_AVAILABLE = False

__all__ = ['CLI']

# Add GUI components if available
if 'PYQT_AVAILABLE' in locals() and PYQT_AVAILABLE:
    __all__.extend(['MainWindow', 'run_gui', 'PYQT_AVAILABLE'])
