from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import VAULT_CHANNEL_ID
from database import add_video


async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only process messages from vault channel
    if not update.effective_chat:
        return

    if update.effective_chat.id != VAULT_CHANNEL_ID:
        return

    msg = update.effective_message

    # Only process videos or files
    if msg.video or msg.document or msg.video_note:
        try:
            await add_video(msg.message_id)
        except Exception as e:
            print(f"Error adding video to DB: {e}")


# Export handler for handlers/__init__.py
uploader_handler = MessageHandler(
    filters.ChatType.CHANNEL
    & (
        filters.VIDEO
        | filters.Document.ALL
        | filters.VIDEO_NOTE
    ),
    handle_channel_post,
)
