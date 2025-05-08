"""
Super simple test script to check if Python is working.
"""

import logging
import sys
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Test function to check Python execution"""
    logger.info("Simple test script")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info("Script is working!")

if __name__ == "__main__":
    main()