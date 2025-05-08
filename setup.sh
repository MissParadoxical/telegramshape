#!/bin/bash
# Simple setup script for kids to get started with the bot

echo "==================================================="
echo "          SETUP TELEGRAM SHAPE BOT                 "
echo "==================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker isn't installed! You need to install Docker first."
    echo "   Go to https://docs.docker.com/get-docker/ to download it."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose isn't installed! You need it to run this bot."
    echo "   Usually it comes with Docker Desktop."
    exit 1
fi

# Check for .env file and create if not present
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    
    if [ ! -f ".env.example" ]; then
        echo "❌ .env.example file is missing! Cannot continue."
        exit 1
    fi
    
    # Copy the example file
    cp .env.example .env
    
    # Get Telegram token
    echo ""
    echo "🤖 Let's set up your Telegram bot!"
    echo "   First, you need a bot token from @BotFather on Telegram."
    echo ""
    read -p "Enter your Telegram bot token: " telegram_token
    
    # Get Shape name
    echo ""
    echo "✨ Now, enter your Shape name (like shapesinc/your-shape-name)"
    echo "   If you don't have one, just press Enter to use the default."
    echo ""
    read -p "Enter your Shape name: " shape_name
    
    # Set the values in .env
    if [ ! -z "$telegram_token" ]; then
        sed -i "s/TELEGRAM_TOKEN=.*/TELEGRAM_TOKEN=$telegram_token/" .env
    fi
    
    if [ ! -z "$shape_name" ]; then
        sed -i "s/SHAPES_MODEL=.*/SHAPES_MODEL=$shape_name/" .env
    fi
    
    echo "✅ .env file created and updated!"
else
    echo "✅ .env file already exists!"
fi

# Create data directory
mkdir -p data
echo "✅ Created data directory for the database!"

# Build and start the bot
echo ""
echo "🚀 Building and starting your bot..."
docker-compose up -d

echo ""
echo "✅ All done! Your bot should be running now."
echo "   Users can talk to your bot on Telegram and use /register to add their Shapes API keys."
echo ""
echo "   To stop the bot, run: docker-compose down"
echo "   To see logs, run: docker-compose logs -f"
echo ""