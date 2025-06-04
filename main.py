import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    group_link = os.getenv("GROUP_LINK")

    if group_link:
        message = (
            f"Hi {user.first_name}, welcome to The Snug! 🦥\n\n"
            f"Here’s your one-time access link to join the private group:\n{group_link}\n\n"
            f"Please do not share this link — it's just for you!"
        )
    else:
        message = (
            f"Hi {user.first_name}, welcome to The Snug! 🦥\n\n"
            "Unfortunately, the invite link is currently unavailable. Please try again later."
        )

    await update.message.reply_text(message)


# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Bot is running...")
    app.run_polling()
