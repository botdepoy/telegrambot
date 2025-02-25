import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from Railway environment variables
TOKEN = os.getenv("TOKEN")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text("Hello! I am your bot. Type /help to see available commands.")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Handles the /help command."""
    await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Get help")

async def run_bot():
    """Start the bot without closing the running event loop."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Bot is running...")

    try:
        await app.initialize()  # Ensure the bot is properly initialized
        await app.run_polling()  # Start the bot in polling mode
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await app.shutdown()  # Ensure a clean shutdown

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(loop)  # Set the new event loop
        loop.run_until_complete(run_bot())  # Run bot in this event loop
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
