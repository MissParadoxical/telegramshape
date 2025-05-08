# Shape on Telegram

A Telegram bot that connects users to their personal Shapes API. This bot allows users to interact with a Shapes language model through Telegram using their own API keys.

## Features

- Connect Telegram users to their personal Shapes API
- Each user registers their own API key (done in private DMs for security)
- Bot responds to mentions, replies, and direct messages
- Stateless design - no conversation history needed
- Simple database to store user API keys
- OpenAI SDK compatibility

## Commands

- `/start` - Get started with the bot
- `/help` - Show all available commands
- `/register` - Register your Shapes API key (DM only)
- `/wack` - Restart your Shape

## Setup & Installation

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install python-telegram-bot python-dotenv openai
   ```
3. Create a `.env` file based on `.env.example`:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   SHAPES_MODEL=shapesinc/shape-username
   SHAPES_API_URL=https://api.shapes.inc/v1/
   DB_FILE=shape_bot.db
   ```
4. Run the bot:
   ```
   python main.py
   ```

### Docker Deployment

1. Make sure Docker and Docker Compose are installed on your system
2. Create a `.env` file with your environment variables (same as above)
3. Run with Docker Compose:
   ```
   docker-compose up -d
   ```

## How to Get Started

1. Create a new bot via Telegram's [BotFather](https://t.me/botfather)
2. Get your Telegram bot token and add it to `.env`
3. Get your Shapes API key from [Shapes Inc](https://shapes.inc)
4. Start the bot
5. Send the `/register` command to your bot in a private message
6. Follow the instructions to save your API key
7. Start chatting with your Shape!

## Directory Structure

- `main.py` - Entry point for the bot
- `bot.py` - Main bot logic and command handlers
- `api_handler.py` - Handles API requests to Shapes API
- `db.py` - Database functionality for API key storage
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration

## Customization

You can customize the Shapes model by changing the `SHAPES_MODEL` environment variable in your `.env` file without any code changes.

## License

MIT