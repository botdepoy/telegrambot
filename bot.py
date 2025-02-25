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
    """Start the bot properly without closing event loops."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Bot is running...")

    try:
        await app.run_polling()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await app.shutdown()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.info("Event loop is already running, using create_task...")
            loop.create_task(run_bot())  # Run bot in the existing event loop
        else:
            logger.info("No running event loop found, creating new event loop...")
            loop.run_until_complete(run_bot())  # Start a new event loop
    except RuntimeError:
        asyncio.run(run_bot())  # Ensure proper execution
