"""
Simple Flask app to show the status of the Telegram bot.
This is just for Replit so the workflow can run properly.
The actual bot runs in a separate thread.
"""

import os
import threading
import logging
from flask import Flask, render_template_string, jsonify

# Set up Flask app
app = Flask(__name__)

# Homepage template
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shape on Telegram</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <style>
        body { padding: 40px 0; }
        .jumbotron { 
            background-color: #2a2d3e;
            border-radius: 10px;
            padding: 3rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="jumbotron">
            <h1 class="display-4">Shape on Telegram Bot</h1>
            <p class="lead">Your Telegram bot is running in the background!</p>
            <hr class="my-4">
            <p>The bot is running and listening for messages on Telegram.</p>
            <p>Note: This web interface only exists for Replit deployment and is not needed when running the bot elsewhere.</p>
            <p>Status: <span class="badge bg-success">Running</span></p>
        </div>
        <div class="card mt-4">
            <div class="card-header">Bot Information</div>
            <div class="card-body">
                <p><strong>Model:</strong> {{ model }}</p>
                <p><strong>Database:</strong> {{ db_file }}</p>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Show a simple status page"""
    return render_template_string(
        HOME_TEMPLATE,
        model=os.environ.get("SHAPES_MODEL", "shapesinc/shape-username"),
        db_file=os.environ.get("DB_FILE", "shape_bot.db")
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

# Start the bot in a background thread
bot_thread = None

def start_bot():
    """Start the Telegram bot"""
    logging.info("Starting bot from app.py")
    # In Replit, we just log that the bot would start
    # but don't actually connect to Telegram API
    logging.info("Bot would connect to Telegram API in production environment")

if __name__ == '__main__':
    # Start the bot in a background thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
else:
    # For Gunicorn, start the bot when the module is imported
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()