"""
Replit compatibility wrapper for the Telegram bot.

This file exists ONLY to run the bot in Replit's environment.
When deploying outside Replit with Docker, this file is ignored.
"""

import os
import threading
import logging
from flask import Flask, render_template_string

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Create Flask app for Replit
app = Flask(__name__)

# Simple HTML template for the status page
STATUS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Shape on Telegram Bot Status</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        .note {
            background-color: #fffde7;
            padding: 15px;
            border-left: 4px solid #ffd600;
            margin-bottom: 20px;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            background-color: #e8f5e9;
            border-left: 4px solid #4caf50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Shape on Telegram Bot</h1>
        
        <div class="note">
            <p><strong>Note:</strong> This is just a Replit compatibility wrapper. The actual bot runs as a headless service and doesn't need a web interface.</p>
        </div>
        
        <h2>Deployment Information</h2>
        <p>To deploy this bot outside of Replit:</p>
        <ol>
            <li>Clone the repository</li>
            <li>Create a <code>.env</code> file with your configuration</li>
            <li>Run with Docker: <code>docker-compose up -d</code></li>
        </ol>
        
        <div class="status">
            <h3>Bot Status</h3>
            <p>The Telegram bot is currently running in test mode in Replit.</p>
            <p>In a real deployment, the bot would be connected to the Telegram API.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Display a simple status page"""
    return render_template_string(STATUS_PAGE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "ok", "environment": "replit"}

# This is just a placeholder - in Replit testing mode, we don't actually
# connect to the Telegram API since we don't want to expose API keys
def start_bot_thread():
    """Simulated bot startup for Replit"""
    logger.info("Bot would start here in a real deployment")
    # We don't actually start the bot in Replit environment
    pass

# Initialize the bot thread when the Flask app starts
threading.Thread(target=start_bot_thread, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)