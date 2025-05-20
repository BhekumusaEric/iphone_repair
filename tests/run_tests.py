#!/usr/bin/env python3
"""
run_tests.py - Run all tests for the iPhone Boot Recovery Tool

This script runs all tests for the iPhone Boot Recovery Tool and generates
a coverage report.
"""

import os
import sys
import unittest
import coverage

# Start coverage
cov = coverage.Coverage(
    source=["src"],
    omit=["*/__init__.py", "*/gui.py"]
)
cov.start()

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_diagnostic import TestDiagnosticTool
from test_recovery import TestRecoveryTool
from test_advanced_recovery import TestAdvancedRecovery
from test_device_communication import TestDeviceCommunication

# Create test suite
def create_test_suite():
    """Create a test suite with all tests"""
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestDiagnosticTool))
    test_suite.addTest(unittest.makeSuite(TestRecoveryTool))
    test_suite.addTest(unittest.makeSuite(TestAdvancedRecovery))
    test_suite.addTest(unittest.makeSuite(TestDeviceCommunication))
    
    return test_suite

if __name__ == "__main__":
    # Create and run test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(create_test_suite())
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    # Print coverage report
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory="coverage_html")
    print(f"HTML coverage report generated in {os.path.abspath('coverage_html')}")
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
