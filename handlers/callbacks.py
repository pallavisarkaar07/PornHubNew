from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import *
from database import (
    is_banned,
    is_sudo,
    get_all_videos,
    get_user_seen,
    reset_user_seen,
    add_user_seen,
)
from utils import is_on_cooldown
import random


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    bot_name = (await context.bot.get_me()).first_name

    caption = (
        f"🥵 Welcome to {bot_name}!\n"
        "Here you will access the most unseen videos.\n"
        "👇 Tap below to explore:"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📩 Get Random Video",
                callback_data="get_video"
            )
        ],
        [
            InlineKeyboardButton(
                "Developer",
                url=DEVELOPER_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "Support",
                url=SUPPORT_LINK
            ),
            InlineKeyboardButton(
                "Help",
                callback_data="show_privacy_info"
            ),
        ],
    ])

    await query.edit_message_media(
        media=InputMediaPhoto(
            media=WELCOME_IMAGE,
            caption=caption
        ),
        reply_markup=keyboard,
    )


async def callback_get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id

    await query.answer()

    if await is_banned(uid):
        await query.message.reply_text(
            "🚫 You are banned from using this bot."
        )
        return

    on_cd, wait = is_on_cooldown(uid, COOLDOWN_SECONDS)

    if not (await is_sudo(uid)) and on_cd:
        await query.message.reply_text(
            f"⏳ Please wait {wait} seconds before getting another video."
        )
        return

    all_videos = await get_all_videos()

    if not all_videos:
        await query.message.reply_text(
            "⚠️ Sorry, no videos available yet."
        )
        return

    user_seen = await get_user_seen(uid)

    unseen = list(set(all_videos) - set(user_seen))

    if not unseen:
        await query.message.reply_text(
            "✅ You watched all videos! Resetting list."
        )

        await reset_user_seen(uid)
        unseen = all_videos.copy()

    random.shuffle(unseen)

    chosen_message_id = unseen[0]

    try:
        await context.bot.copy_message(
            chat_id=uid,
            from_chat_id=VAULT_CHANNEL_ID,
            message_id=chosen_message_id,
        )

    except Exception as e:
        await query.message.reply_text(
            f"⚠️ Error sending video:\n{e}"
        )
        return

    await add_user_seen(uid, chosen_message_id)


async def show_privacy_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "⚠️ Privacy & Terms\n\n"
        "Please use this bot responsibly."
    )


# Export handlers for handlers/__init__.py
callback_handlers = [
    CallbackQueryHandler(
        callback_get_video,
        pattern="^get_video$"
    ),
    CallbackQueryHandler(
        back_to_start,
        pattern="^back_start$"
    ),
    CallbackQueryHandler(
        show_privacy_info,
        pattern="^show_privacy_info$"
    ),
]
