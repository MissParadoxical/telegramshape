#!/bin/bash
# Simple script to start the Telegram bot

# Print header
echo "==================================================="
echo "            STARTING SHAPE ON TELEGRAM             "
echo "==================================================="

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your actual values."
        echo "You need to set:"
        echo "  - TELEGRAM_TOKEN (get from @BotFather)"
        echo "  - SHAPES_MODEL (your shape name)"
        exit 1
    else
        echo "❌ No .env.example found either! Cannot continue."
        exit 1
    fi
fi

# Create data directory if it doesn't exist
mkdir -p data

# Start the bot
echo "🚀 Starting the bot..."
python main.py