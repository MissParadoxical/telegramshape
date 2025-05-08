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
        "👋 Hey there! I'm your Shapes connector bot.\n\n"
        "To use me, you'll need to register your Shapes API key first.\n"
        "Use /register to do that in a private message.\n\n"
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
        "🔍 *Shape Bot Help*\n\n"
        "I connect you to your Shapes API. Here's what I can do:\n\n"
        "🔑 */register* - Register your Shapes API key (DM only)\n"
        "🔄 */wack* - Restart your Shape\n"
        "❓ */help* - Show this help message\n\n"
        "Once you've registered your API key, you can interact with me in any chat by:\n"
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
            "🔒 For security reasons, please send me a direct message to register your API key."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "🔑 Please send me your Shapes API key.\n\n"
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
        "✅ Your API key has been registered successfully!\n\n"
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
            "❌ You don't have an API key registered yet.\n"
            "Please use /register to set up your key first."
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
            "❌ You don't have an API key registered yet.\n"
            "Please use /register to set up your key first."
        )
        return
    
    # Get the message text
    message_text = update.message.text
    
    # If this is a group chat and the bot was mentioned, remove the mention
    if update.effective_chat.type != "private" and context.bot.username:
        # Pattern to match @botusername with or without a space after
        bot_mention_pattern = rf'@{context.bot.username}\s*'
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
    
    # Message handlers
    application.add_handler(MessageHandler(
        (filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE), 
        handle_message
    ))
    application.add_handler(MessageHandler(
        (filters.TEXT & filters.Entity("mention") & ~filters.COMMAND), 
        handle_message
    ))
    application.add_handler(MessageHandler(
        (filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS & filters.REPLY), 
        handle_message
    ))
    
    # Start the bot
    logger.info("Starting the bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
