from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# 🔹 Replace with your actual Telegram bot token and chat ID
BOT_TOKEN = "7680394855:AAFVjKErGVwWg9bZ49BnChVgCLnv1xA3MRw"
CHAT_ID = "8101143576"  # Your Telegram ID or group ID

# 🔹 Form Web App URL
WEB_APP_URL = "https://botdepoy.github.io/telegrambot/index.html"

# 🔹 Initialize Flask App
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)


def start(update: Update, context: CallbackContext):
    """Handles /start command and displays a button to open the form."""
    keyboard = [[InlineKeyboardButton("填写信息 (Fill Form)", web_app={"url": WEB_APP_URL})]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("点击下方按钮填写信息 (Click the button below to fill out the form)", reply_markup=reply_markup)


@app.route("/", methods=["GET"])
def home():
    return "Telegram Bot is Running 🚀"


@app.route("/submit", methods=["POST"])
def receive_form_data():
    """Receives form submission and sends it to Telegram."""
    data = request.json

    # Extract form data
    name = data.get("name", "N/A")
    email = data.get("email", "N/A")
    user_id = data.get("user_id", "N/A")
    username = data.get("username", "N/A")
    first_name = data.get("first_name", "N/A")

    # Create message
    message = f"📩 **New Form Submission**\n\n"
    message += f"👤 Name: {name}\n📧 Email: {email}\n"
    message += f"🆔 User ID: {user_id}\n👤 Username: @{username}\n"
    message += f"📝 First Name: {first_name}"

    # Send message to Telegram
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

    return {"status": "success", "message": "Data sent to Telegram"}


if __name__ == "__main__":
    # Set webhook (optional)
    bot.setWebhook(url="https://telegrambot-n4a3.onrender.com")

    # Start the bot using Flask
    app.run(host="0.0.0.0", port=5000)
