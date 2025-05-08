#!/bin/bash

# Simple run script for the Telegram Shape Bot
echo "🤖 Starting Telegram Shape Bot..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed! Please install Python 3.11 or newer."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking for required packages..."
python -c "import telegram" &> /dev/null || { echo "❌ python-telegram-bot not found! Run: pip install python-telegram-bot"; exit 1; }
python -c "import dotenv" &> /dev/null || { echo "❌ python-dotenv not found! Run: pip install python-dotenv"; exit 1; }
python -c "import openai" &> /dev/null || { echo "❌ openai not found! Run: pip install openai"; exit 1; }

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your actual tokens and API keys."
        echo "🔑 You'll need to set TELEGRAM_TOKEN at minimum."
        exit 1
    else
        echo "❌ .env.example not found! Cannot create .env file."
        exit 1
    fi
fi

# Start the bot
echo "🚀 Starting the bot..."
python main.py