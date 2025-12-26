import os
import yt_dlp
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ──────────────────────────────
# Metadata formatter
# ──────────────────────────────
def build_caption(info, user):
    return (
        f"🎵 *Title:* {info.get('title')}\n"
        f"📺 *Channel:* {info.get('uploader')}\n"
        f"📂 *Category:* {info.get('categories', ['N/A'])[0]}\n"
        f"📅 *Upload Date:* {info.get('upload_date')}\n"
        f"⏰ *Duration:* {info.get('duration_string')}\n"
        f"👀 *Views:* {info.get('view_count')}\n"
        f"👍 *Likes:* {info.get('like_count')}\n"
        f"👎 *Dislikes:* {info.get('dislike_count', 'Hidden')}\n"
        f"💬 *Comments:* {info.get('comment_count')}\n"
        f"📦 *File Size:* {round(info.get('filesize', 0) / 1024 / 1024, 2)} MB\n"
        f"⚖️ *License:* {info.get('license', 'Standard')}\n"
        f"🔞 *Age Restricted:* {info.get('age_limit', 0) > 0}\n\n"
        f"🙋 *Requested by:* {user.mention_html()}"
    )

def dev_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2")]]
    )

# ──────────────────────────────
# /song command
# ──────────────────────────────
async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /song <song name or url>")
        return

    query = " ".join(context.args)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    await update.message.reply_text("🎧 Downloading song...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info)

    caption = build_caption(info, update.message.from_user)

    await update.message.reply_audio(
        audio=open(file_path, "rb"),
        caption=caption,
        parse_mode="HTML",
        reply_markup=dev_button()
    )

    os.remove(file_path)

# ──────────────────────────────
# /video command
# ──────────────────────────────
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /video <video name or url>")
        return

    query = " ".join(context.args)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    await update.message.reply_text("🎬 Downloading video...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info)

    caption = build_caption(info, update.message.from_user)

    await update.message.reply_video(
        video=open(file_path, "rb"),
        caption=caption,
        parse_mode="HTML",
        reply_markup=dev_button()
    )

    os.remove(file_path)

# ──────────────────────────────
# Main
# ──────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("song", song))
    app.add_handler(CommandHandler("video", video))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
