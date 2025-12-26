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

# ──────────────────────────────
# Load config
# ──────────────────────────────
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ──────────────────────────────
# Helpers
# ──────────────────────────────
def dev_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2")]]
    )

def build_caption(info, user):
    filesize = info.get("filesize") or info.get("filesize_approx") or 0
    filesize_mb = round(filesize / 1024 / 1024, 2)

    return (
        f"🎵 *Title:* {info.get('title', 'N/A')}\n"
        f"📺 *Channel:* {info.get('uploader', 'N/A')}\n"
        f"📂 *Category:* {info.get('categories', ['N/A'])[0]}\n"
        f"📅 *Upload Date:* {info.get('upload_date', 'N/A')}\n"
        f"⏰ *Duration:* {info.get('duration_string', 'N/A')}\n"
        f"👀 *Views:* {info.get('view_count', 'N/A')}\n"
        f"👍 *Likes:* {info.get('like_count', 'Hidden')}\n"
        f"💬 *Comments:* {info.get('comment_count', 'Hidden')}\n"
        f"📦 *File Size:* {filesize_mb} MB\n"
        f"⚖️ *License:* {info.get('license', 'Standard')}\n"
        f"🔞 *Age Restricted:* {'Yes' if info.get('age_limit', 0) > 0 else 'No'}\n\n"
        f"🙋 *Requested by:* {user.mention_markdown()}"
    )

def get_search_query(query: str) -> str:
    if query.startswith("http://") or query.startswith("https://"):
        return query
    return f"ytsearch1:{query}"

# ──────────────────────────────
# Commands
# ──────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome!*\n\n"
        "🎵 `/song <name or url>` – Download song\n"
        "🎬 `/video <name or url>` – Download video\n\n"
        "Example:\n"
        "`/song sanam re`\n"
        "`/video arijit singh`\n\n"
        "🚀 Powered by @deweni2",
        parse_mode="Markdown",
        reply_markup=dev_button()
    )

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/song <song name or url>`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    search_query = get_search_query(query)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    await update.message.reply_text("🎧 Searching & downloading song...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)

            if "entries" in info:
                info = info["entries"][0]

            file_path = ydl.prepare_filename(info)

        caption = build_caption(info, update.message.from_user)

        await update.message.reply_audio(
            audio=open(file_path, "rb"),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=dev_button()
        )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n`{str(e)}`", parse_mode="Markdown")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/video <video name or url>`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    search_query = get_search_query(query)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    await update.message.reply_text("🎬 Searching & downloading video...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)

            if "entries" in info:
                info = info["entries"][0]

            file_path = ydl.prepare_filename(info)

        caption = build_caption(info, update.message.from_user)

        await update.message.reply_video(
            video=open(file_path, "rb"),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=dev_button()
        )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n`{str(e)}`", parse_mode="Markdown")

# ──────────────────────────────
# Main
# ──────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song))
    app.add_handler(CommandHandler("video", video))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
