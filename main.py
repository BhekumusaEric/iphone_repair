#!/usr/bin/env python3
"""
main.py - Main entry point for iPhone Boot Recovery Tool

This script launches the iPhone Boot Recovery Tool with the appropriate
user interface based on the environment and command-line arguments.
"""

import os
import sys
import argparse
from typing import List, Optional

from src.ui.cli import CLI

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
        "--debug", 
        action="store_true",
        help="Enable debug mode with verbose logging"
    )
    
    parser.add_argument(
        "--simulate", 
        action="store_true",
        help="Run in simulation mode without actual device communication"
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
    
    # In a full implementation, we would check for GUI capabilities
    # and launch the appropriate interface. For now, we only have CLI.
    
    # Launch CLI
    cli = CLI()
    cli.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
