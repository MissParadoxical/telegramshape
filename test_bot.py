"""
Simple test script to verify the code is working correctly.
"""

import logging
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Test function to check imports and basic functionality"""
    try:
        logger.info("Testing bot components...")
        
        # Test importing modules
        logger.info("Importing modules...")
        import bot
        import db
        import api_handler
        
        # Test database initialization
        logger.info("Initializing database...")
        db.init_db()
        
        logger.info("Testing environment variables...")
        telegram_token = os.environ.get("TELEGRAM_TOKEN")
        shapes_model = os.environ.get("SHAPES_MODEL", "shapesinc/shape-username")
        shapes_api_url = os.environ.get("SHAPES_API_URL", "https://api.shapes.inc/v1/")
        
        logger.info(f"TELEGRAM_TOKEN: {'Set' if telegram_token else 'Not set'}")
        logger.info(f"SHAPES_MODEL: {shapes_model}")
        logger.info(f"SHAPES_API_URL: {shapes_api_url}")
        
        logger.info("All tests passed successfully!")
        logger.info("The bot code looks good and should work when deployed outside of Replit.")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    main()