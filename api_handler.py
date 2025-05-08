import os
import logging
from openai import OpenAI

# Set up logging
logger = logging.getLogger(__name__)

# Get the model name from environment variables with a default fallback
SHAPES_MODEL = os.environ.get("SHAPES_MODEL", "shapesinc/shape-username")
SHAPES_API_URL = os.environ.get("SHAPES_API_URL", "https://api.shapes.inc/v1/")

def process_message(message_text, api_key):
    """
    Send the message to the Shapes API using the OpenAI SDK compatibility
    
    Args:
        message_text (str): The message to process
        api_key (str): The user's API key
        
    Returns:
        str: The response from the API
    """
    try:
        # Create client with user's API key
        client = OpenAI(api_key=api_key, base_url=SHAPES_API_URL)
        
        # Send the message to the Shapes API
        logger.info(f"Sending message to Shapes API using model: {SHAPES_MODEL}")
        response = client.chat.completions.create(
            model=SHAPES_MODEL,
            messages=[{"role": "user", "content": message_text}]
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        logger.info("Successfully received response from Shapes API")
        return response_text
    
    except Exception as e:
        logger.error(f"Error processing message with Shapes API: {str(e)}")
        return f"Sorry, I had trouble processing your request. Error: {str(e)}"

def send_wack(api_key):
    """
    Send a !wack command to restart the model
    
    Args:
        api_key (str): The user's API key
        
    Returns:
        str: The response from the API
    """
    try:
        # Create client with user's API key
        client = OpenAI(api_key=api_key, base_url=SHAPES_API_URL)
        
        # Send the !wack command
        logger.info("Sending !wack command to Shapes API")
        response = client.chat.completions.create(
            model=SHAPES_MODEL,
            messages=[{"role": "user", "content": "!wack"}]
        )
        
        # Extract the response content
        response_text = response.choices[0].message.content
        logger.info("Successfully sent !wack command")
        return response_text
    
    except Exception as e:
        logger.error(f"Error sending !wack command: {str(e)}")
        return f"Sorry, I had trouble processing your !wack command. Error: {str(e)}"
