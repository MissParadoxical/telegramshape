import logging
import threading
import os
from flask import Flask, render_template_string, jsonify
from bot import run_bot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create Flask app
app = Flask(__name__)

# HTML template for the home page
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shape on Telegram</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <style>
        body {
            padding: 40px 0;
        }
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
            <h1 class="display-4">Shape on Telegram</h1>
            <p class="lead">Your Telegram bot connecting users to their personal Shapes API is running!</p>
            <hr class="my-4">
            <p>The bot is actively listening for messages on Telegram. Users can interact with it using the following commands:</p>
            <ul>
                <li><code>/start</code> - Get started with the bot</li>
                <li><code>/help</code> - Show all available commands</li>
                <li><code>/register</code> - Register your Shapes API key (DM only)</li>
                <li><code>/wack</code> - Restart your Shape</li>
            </ul>
            <p>Status: <span class="badge bg-success">Running</span></p>
        </div>
        
        <div class="card mt-4">
            <div class="card-header">
                Bot Information
            </div>
            <div class="card-body">
                <p><strong>Model:</strong> {{ model }}</p>
                <p><strong>API URL:</strong> {{ api_url }}</p>
                <p><strong>Database:</strong> {{ db_file }}</p>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Display the home page with bot information"""
    return render_template_string(
        HOME_TEMPLATE,
        model=os.environ.get("SHAPES_MODEL", "shapesinc/shape-username"),
        api_url=os.environ.get("SHAPES_API_URL", "https://api.shapes.inc/v1/"),
        db_file=os.environ.get("DB_FILE", "shape_bot.db")
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

def run_flask():
    """Run the Flask web server"""
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run the Flask app in the main thread
    run_flask()
