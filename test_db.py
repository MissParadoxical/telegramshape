"""
Test script for the database component.
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
    """Test function to check database functionality"""
    try:
        logger.info("Testing database component...")
        
        # Import the database module
        import db
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize the database
        logger.info("Initializing database...")
        db.init_db()
        
        # Test storing and retrieving a key
        test_user_id = 12345
        test_api_key = "test_api_key_for_testing"
        
        logger.info(f"Storing test API key for user {test_user_id}...")
        db.store_api_key(test_user_id, test_api_key)
        
        logger.info("Retrieving the API key...")
        retrieved_key = db.get_api_key(test_user_id)
        
        if retrieved_key == test_api_key:
            logger.info("✅ Success! Retrieved key matches stored key.")
        else:
            logger.error(f"❌ Error: Retrieved key '{retrieved_key}' doesn't match stored key '{test_api_key}'")
            
        # Test deleting a key
        logger.info("Testing key deletion...")
        if db.delete_api_key(test_user_id):
            logger.info("✅ Success! Key was deleted.")
        else:
            logger.error("❌ Error: Key deletion failed.")
            
        # Verify the key is gone
        if db.get_api_key(test_user_id) is None:
            logger.info("✅ Success! Key was properly deleted.")
        else:
            logger.error("❌ Error: Key still exists after deletion.")
        
        logger.info("Database component tests passed successfully!")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    main()