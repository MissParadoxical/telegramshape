# Shape on Telegram Bot - Deployment Guide

## Essential Files for Deployment

For deploying this bot outside of Replit, you only need these core files:

```
├── main.py           # Main entry point
├── bot.py            # Core Telegram bot functionality
├── db.py             # Database functions for API key storage
├── api_handler.py    # Integration with the Shapes API
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── .env.example      # Template for creating your .env file
├── setup.sh          # Helper script for setup
├── start_bot.sh      # Helper script for starting the bot
└── README.md         # Documentation
```

## Files to Ignore

The following files were created only for testing in Replit and can be safely ignored:

```
├── app.py            # Flask app for Replit compatibility 
├── replit_app.py     # Replit compatibility wrapper
├── test_api_handler.py # Test for API handler component
├── test_bot.py       # Test for bot functionality
├── test_db.py        # Test for database component
├── simple_test.py    # Simple test script
└── .replit           # Replit configuration files
```

## Deployment Steps

1. Clone the repository
2. Create a `.env` file with your configuration (based on `.env.example`)
3. Run with Docker: `docker-compose up -d`

## Environment Variables

The bot requires the following environment variables:

- `TELEGRAM_TOKEN`: Your Telegram bot token from BotFather
- `SHAPES_MODEL`: The Shapes API model to use (default: "shapesinc/shape-username")
- `SHAPES_API_URL`: The Shapes API URL (default: "https://api.shapes.inc/v1/")
- `DB_FILE`: Path to the SQLite database file (default: "shape_bot.db")

## Using the Bot

1. Start a conversation with your bot on Telegram
2. Use the `/register` command to store your Shapes API key
3. Send messages to the bot and it will process them with the Shapes API
4. Use `/wack` to restart the model when needed
5. Use `/help` to see available commands