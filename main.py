#!/usr/bin/env python3
"""
main.py - Main entry point for iPhone Boot Recovery Tool

This script launches the iPhone Boot Recovery Tool with the appropriate
user interface based on the environment and command-line arguments.
"""

import os
import sys
import argparse
import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import UI modules
from src.ui.cli import CLI

# Try to import GUI modules
try:
    from src.ui.gui import run_gui, PYQT_AVAILABLE
except ImportError:
    logger.warning("GUI modules not available")
    PYQT_AVAILABLE = False

def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse command-line arguments

    Args:
        args: Command-line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="iPhone Boot Recovery Tool - Recover iPhones stuck on Apple logo"
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        help="Force command-line interface mode"
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Force graphical user interface mode"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose logging"
    )

    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Run in simulation mode without actual device communication"
    )

    parser.add_argument(
        "--advanced",
        action="store_true",
        help="Enable advanced recovery techniques"
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests"
    )

    return parser.parse_args(args)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point

    Args:
        args: Command-line arguments

    Returns:
        int: Exit code
    """
    if args is None:
        args = sys.argv[1:]

    parsed_args = parse_args(args)

    # Set debug logging if requested
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Run tests if requested
    if parsed_args.test:
        logger.info("Running tests...")
        try:
            from tests.run_tests import create_test_suite
            import unittest

            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(create_test_suite())

            return 0 if result.wasSuccessful() else 1
        except ImportError as e:
            logger.error(f"Error importing test modules: {e}")
            return 1

    # Determine which UI to use
    use_gui = False

    if parsed_args.gui:
        # User explicitly requested GUI
        if PYQT_AVAILABLE:
            use_gui = True
        else:
            logger.warning("GUI requested but not available, falling back to CLI")
    elif parsed_args.cli:
        # User explicitly requested CLI
        use_gui = False
    else:
        # Auto-detect
        use_gui = PYQT_AVAILABLE and sys.stdout.isatty() and not os.environ.get("DISPLAY") is None

    # Launch appropriate UI
    if use_gui:
        logger.info("Launching GUI...")
        return run_gui()
    else:
        logger.info("Launching CLI...")
        cli = CLI()
        cli.run()
        return 0

if __name__ == "__main__":
    sys.exit(main())
