import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram Bot Token from Railway's environment variables
TOKEN = os.getenv("TOKEN")  # Ensure TOKEN is set in Railway

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user IDs in a file
USER_DATA_FILE = "user_ids.txt"

# Load user IDs from file
def load_user_ids():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()

# Save user IDs to file
def save_user_ids(user_ids):
    with open(USER_DATA_FILE, "w") as file:
        for user_id in user_ids:
            file.write(f"{user_id}\n")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_ids = load_user_ids()
    user_ids.add(user_id)
    save_user_ids(user_ids)

    menu_buttons = [
        ["✈ 落地接机", "🔖 证照办理"],
        ["🏤 房产凭租", "🏩 酒店预订"],
        ["🍽️ 食堂信息", "📦 生活物资"],
        ["🔔 后勤生活信息频道"]
    ]
    reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("欢迎使用亚太·亚通机器人！请选择一个选项：", reply_markup=reply_markup)

# Command: /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids = load_user_ids()
    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("用法: /broadcast <消息>")
        return

    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")

    await update.message.reply_text("广播消息已发送给所有用户！")

# Main function to start bot
async def run_bot():
    """Start the bot correctly in an async event loop"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    logger.info("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(run_bot())
        loop.run_forever()
    except RuntimeError:
        asyncio.run(run_bot())
