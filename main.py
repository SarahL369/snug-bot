import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}, welcome to The Snug! 🦥\n\n"
        f"Here's your one-time access link to join the private group:\n{GROUP_LINK}\n\n"
        f"Please do not share this link — it's just for you!"
    )

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Bot is running...")
    app.run_polling()
