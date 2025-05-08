import os
import logging
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)
from dotenv import load_dotenv

from db import init_db, store_api_key, get_api_key, delete_api_key
from api_handler import process_message, send_wack

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Get Telegram bot token from environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("No TELEGRAM_TOKEN found in environment variables!")
    exit(1)

# Conversation states
AWAITING_API_KEY = 1

async def start(update: Update, context: CallbackContext) -> None:
    """
    Handler for the /start command
    """
    await update.message.reply_text(
        "👋 Hey there! Lets chat!\n\n"
        "To use me, you'll need to register your Shapes API key first.\n"
        "Use /register in a private message.\n\n"
        "After registering, you can use me in any chat by:\n"
        "1. Mentioning me (@shapebot your question)\n"
        "2. Replying to my messages\n"
        "3. DMing me directly\n\n"
        "Type /help for more info."
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """
    Handler for the /help command
    """
    await update.message.reply_text(
        "🔍 *Shape Help*\n\n"
        "Here's what I can do:\n\n"
        "🔑 */register* - Register your Shapes account (DM only)\n"
        "🔄 */wack* - Restart your chat\n"
        "❓ */help* - Show this help message\n\n"
        "Once you've registered, you can interact with me in any chat by:\n"
        "- Mentioning me: @shapebot hello there\n"
        "- Replying to my messages\n"
        "- Sending me direct messages\n\n"
        "Remember: Each message is processed independently - I don't keep conversation history.",
        parse_mode="Markdown"
    )

async def register_command(update: Update, context: CallbackContext) -> int:
    """
    Start the registration process to store the user's API key
    """
    # Only allow registration in private chats
    if update.effective_chat.type != "private":
        await update.message.reply_text(
            "🔒 For security reasons, please send me a direct message to register."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "🔑 Please send me your Shapes account wide API key from https://shapes.inc/developer.\n\n"
        "I'll store it securely to connect you to your Shape.\n"
        "You can cancel anytime with /cancel."
    )
    return AWAITING_API_KEY

async def process_api_key(update: Update, context: CallbackContext) -> int:
    """
    Process and store the provided API key
    """
    user_id = update.effective_user.id
    api_key = update.message.text.strip()
    
    # Basic validation - API keys typically have a minimum length
    # and follow specific formats, but this is a simple check
    if len(api_key) < 10:
        await update.message.reply_text(
            "⚠️ That doesn't look like a valid API key. Please try again or use /cancel."
        )
        return AWAITING_API_KEY
    
    # Store the API key
    store_api_key(user_id, api_key)
    
    await update.message.reply_text(
        "✅ You have been registered successfully!\n\n"
        "You can now use me in any chat by:\n"
        "- Mentioning me\n"
        "- Replying to my messages\n"
        "- Sending me direct messages\n\n"
        "Try it out with a simple message!"
    )
    return ConversationHandler.END

async def cancel_registration(update: Update, context: CallbackContext) -> int:
    """
    Cancel the registration process
    """
    await update.message.reply_text(
        "🚫 Registration cancelled. You can use /register anytime to try again."
    )
    return ConversationHandler.END

async def wack_command(update: Update, context: CallbackContext) -> None:
    """
    Handle the /wack command to restart the model
    """
    user_id = update.effective_user.id
    api_key = get_api_key(user_id)
    
    if not api_key:
        await update.message.reply_text(
            "❌ You are not registered yet.\n"
            "Please use /register in my Dms to set up your key first."
        )
        return
    
    await update.message.reply_text("🔄 Sending !wack to restart your Shape...")
    
    # Send the !wack command
    response = send_wack(api_key)
    
    await update.message.reply_text(response or "✅ Shape restarted successfully!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """
    Process incoming messages that should be sent to the Shape
    """
    # Get the user ID
    user_id = update.effective_user.id
    
    # Check if the user has registered an API key
    api_key = get_api_key(user_id)
    if not api_key:
        await update.message.reply_text(
            "❌ You are not registered yet.\n"
            "Please use /register in my DMs to set up your key first."
        )
        return
    
    # Get the message text
    message_text = update.message.text
    
    # In group chats, verify this message is actually for this bot
    if update.effective_chat.type != "private":
        # Get the bot's username
        bot_username = context.bot.username
        
        # Check if this is a mention or a reply
        is_mention = bot_username and f"@{bot_username}" in message_text
        is_reply_to_bot = (update.message.reply_to_message and 
                          update.message.reply_to_message.from_user and
                          update.message.reply_to_message.from_user.id == context.bot.id)
        
        # Only process if it's a direct mention of this bot or a reply to this bot's message
        if not is_mention and not is_reply_to_bot:
            logger.info("Ignoring message in group chat that isn't for this bot")
            return
        
        # If it's a mention, remove the bot's username from the message
        if is_mention and bot_username:
            bot_mention_pattern = rf'@{bot_username}\s*'
            message_text = re.sub(bot_mention_pattern, '', message_text, flags=re.IGNORECASE)
    
    # Process the message with the Shapes API
    response = process_message(message_text, api_key)
    
    # Send the response back to the user
    await update.message.reply_text(response)

def run_bot():
    """
    Initialize and run the Telegram bot
    """
    # Initialize the database
    init_db()
    
    # Create the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add conversation handler for registration
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register_command)],
        states={
            AWAITING_API_KEY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_api_key)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_registration)]
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("wack", wack_command))
    application.add_handler(conv_handler)
    
    # Message handlers for different scenarios
    
    # 1. Direct messages in private chat
    application.add_handler(MessageHandler(
        (filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE), 
        handle_message
    ))
    
    # 2. Messages in group chats - we'll do additional filtering in the handler
    application.add_handler(MessageHandler(
        (filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS), 
        handle_message
    ))
    
    # Start the bot
    logger.info("Starting the bot...")
    
    # When running in a thread from Flask, we need to use asyncio properly
    import asyncio
    import threading
    
    # Check if we're in the main thread or a child thread
    if threading.current_thread() is threading.main_thread():
        # In main thread, we can just run it directly
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        # In a child thread, we need to create and run a new event loop
        try:
            logger.info("Starting bot in a new event loop...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Define the async functions to run
            async def start_application():
                await application.initialize()
                await application.updater.start_polling()
                await application.start()
                logger.info("Bot is now polling for updates...")
                
            # Run the async function in the event loop
            loop.run_until_complete(start_application())
            loop.run_forever()
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}")
            raise
