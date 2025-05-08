# 🤖 Shape on Telegram

A super simple Telegram bot that connects users to their personal Shapes API. Share your Shape with friends on Telegram!

## 🚀 Quick Start

### How to set up (for beginners)

1. **Create a Telegram Bot:**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - **Save the token** it gives you!

2. **Get Your Shape:**
   - If you don't have a Shape yet, get one at [Shapes Inc](https://shapes.inc)
   - Note your Shape name (looks like `shapesinc/your-shape-name`)

3. **Run with Docker (easiest way):**
   - Install [Docker](https://docs.docker.com/get-docker/)
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Telegram token and Shape name
   - Run: `docker-compose up -d`
   - That's it! Your bot is running!

4. **Using the Bot:**
   - Go to your bot on Telegram
   - Type `/start` to see instructions
   - Each user will need to `/register` their own Shapes API key
   - Start chatting!

## ⭐ Features

- Lets users connect to their Shape through Telegram 
- Each user registers their own API key (in DM for security)
- Bot responds to @mentions, replies, and direct messages
- Easy to set up and share with friends

## 💬 Commands

- `/start` - Welcome message and instructions
- `/help` - Show all available commands
- `/register` - Register your Shapes API key (DM only)
- `/wack` - Restart your Shape if it gets confused

## 🔧 Manual Installation

If you don't want to use Docker:

1. Make sure you have Python 3.11+ installed
2. Install dependencies:
   ```
   pip install python-telegram-bot python-dotenv openai
   ```
3. Create a `.env` file with your information
4. Run the bot:
   ```
   python main.py
   ```

## 📝 Customization

You can change the Shape model by editing the `SHAPES_MODEL` in your `.env` file - no code changes needed!

## 🛟 Need Help?

- Check that your `.env` file has the correct information
- Make sure your Telegram token is valid
- Verify that users are using valid Shapes API keys

## 📄 License

MIT - Do whatever you want with this code!