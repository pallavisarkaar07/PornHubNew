from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import *
from config import ADMIN_USER_ID


async def add_sudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("🚫 You are not authorized.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /addsudo <user_id>")
        return

    try:
        user_id = int(context.args[0])
        await add_sudo(user_id)
        await update.message.reply_text(
            f"✅ Added sudo user: {user_id}"
        )
    except Exception:
        await update.message.reply_text(
            "❌ Invalid user ID."
        )


async def remove_sudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("🚫 You are not authorized.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remsudo <user_id>")
        return

    try:
        user_id = int(context.args[0])
        await remove_sudo(user_id)
        await update.message.reply_text(
            f"✅ Removed sudo user: {user_id}"
        )
    except Exception:
        await update.message.reply_text(
            "❌ Invalid user ID."
        )


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID and not await is_sudo(user.id):
        await update.message.reply_text(
            "🚫 You are not authorized."
        )
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /ban <user_id>"
        )
        return

    try:
        user_id = int(context.args[0])
        await add_banned(user_id)

        await update.message.reply_text(
            f"🚫 Banned user: {user_id}"
        )

    except Exception:
        await update.message.reply_text(
            "❌ Invalid user ID."
        )


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID and not await is_sudo(user.id):
        await update.message.reply_text(
            "🚫 You are not authorized."
        )
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /unban <user_id>"
        )
        return

    try:
        user_id = int(context.args[0])
        await remove_banned(user_id)

        await update.message.reply_text(
            f"✅ Unbanned user: {user_id}"
        )

    except Exception:
        await update.message.reply_text(
            "❌ Invalid user ID."
        )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID and not await is_sudo(user.id):
        await update.message.reply_text(
            "🚫 You are not authorized."
        )
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage: /broadcast <message>"
        )
        return

    count = 0

    async for doc in users_col.find({}):
        uid = doc.get("user_id")

        if not uid:
            continue

        try:
            await context.bot.send_message(
                uid,
                text
            )
            count += 1

        except Exception:
            continue

    await update.message.reply_text(
        f"✅ Broadcast sent to {count} users."
    )


# Export handlers for handlers/__init__.py
admin_handlers = [
    CommandHandler("addsudo", add_sudo_command),
    CommandHandler("remsudo", remove_sudo_command),
    CommandHandler("ban", ban_command),
    CommandHandler("unban", unban_command),
    CommandHandler("broadcast", broadcast_command),
]
