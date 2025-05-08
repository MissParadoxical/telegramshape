"""
Main entry point for the Shape on Telegram bot.
This file can be used to run the bot directly or from another module.

In Replit environment, this imports the app from replit_app.py for web interface.
In production deployment, this starts the actual Telegram bot.
"""

import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Determine running environment
IN_REPLIT = os.environ.get("REPL_ID") is not None

# Load environment variables from .env file if it exists
load_dotenv()

# Import app for Replit (gunicorn expects app in main.py)
if IN_REPLIT:
    from replit_app import app
else:
    # When not in Replit, 'app' isn't needed
    pass

def start_bot():
    """
    Print a simple banner and start the bot.
    This function is used when called directly or from another module.
    """
    print("=" * 50)
    print("Starting Shape on Telegram Bot")
    print("=" * 50)
    
    if IN_REPLIT:
        logger.info("Running in Replit environment - bot not actually started")
        logger.info("Use the web interface for demonstration purposes only")
        # In Replit, the bot isn't actually started to avoid API key issues
    else:
        logger.info("Starting bot in production mode")
        # Import and start the bot in production environments
        from bot import run_bot
        run_bot()
    
if __name__ == "__main__":
    start_bot()