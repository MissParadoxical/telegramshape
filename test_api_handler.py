"""
Test script for the API handler component.
"""

import logging
import os
from unittest.mock import patch, MagicMock

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Test function to check API handler functionality"""
    try:
        logger.info("Testing API handler component...")
        
        # Import the API handler module
        import api_handler
        
        # Test environment variables
        logger.info("Checking environment variables...")
        shapes_model = os.environ.get("SHAPES_MODEL", "shapesinc/shape-username")
        shapes_api_url = os.environ.get("SHAPES_API_URL", "https://api.shapes.inc/v1/")
        
        logger.info(f"SHAPES_MODEL: {shapes_model}")
        logger.info(f"SHAPES_API_URL: {shapes_api_url}")
        
        # We can't actually test the API calls without a valid API key,
        # but we can test that the code is structurally correct
        
        logger.info("Testing API handler structure...")
        
        # Verify that the function names and signatures are correct
        assert hasattr(api_handler, 'process_message'), "process_message function missing"
        assert hasattr(api_handler, 'send_wack'), "send_wack function missing"
        
        logger.info("✅ API handler functions exist")
        
        # Mock test for process_message
        with patch('openai.OpenAI') as mock_openai:
            # Create mock response
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = "This is a test response"
            mock_response.choices = [mock_choice]
            
            mock_client.chat.completions.create.return_value = mock_response
            
            # Call the function with test data
            logger.info("Testing process_message with mock data...")
            response = api_handler.process_message("Test message", "fake_api_key")
            
            logger.info(f"Response: {response}")
            
            # Verify mock was called correctly
            mock_openai.assert_called_once()
            mock_client.chat.completions.create.assert_called_once()
            
            logger.info("✅ process_message works with mocked data")
        
        # Mock test for send_wack
        with patch('openai.OpenAI') as mock_openai:
            # Create mock response
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = "Model restarted"
            mock_response.choices = [mock_choice]
            
            mock_client.chat.completions.create.return_value = mock_response
            
            # Call the function with test data
            logger.info("Testing send_wack with mock data...")
            response = api_handler.send_wack("fake_api_key")
            
            logger.info(f"Response: {response}")
            
            # Verify mock was called correctly
            mock_openai.assert_called_once()
            mock_client.chat.completions.create.assert_called_once()
            
            logger.info("✅ send_wack works with mocked data")
        
        logger.info("API handler component tests passed successfully!")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    main()