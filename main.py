import logging

from telegram.ext import ApplicationBuilder

from config import BOT_TOKEN
from handlers import (
    start_handler,
    callback_handlers,
    admin_handlers,
    uploader_handler,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


app = ApplicationBuilder().token(BOT_TOKEN).build()


# Start command handler
app.add_handler(start_handler)


# Callback handlers
for handler in callback_handlers:
    app.add_handler(handler)


# Admin command handlers
for handler in admin_handlers:
    app.add_handler(handler)


# Channel uploader handler
app.add_handler(uploader_handler)


print("🤖 Bot is starting...")

app.run_polling()
