import os
import yt_dlp
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ──────────────────────────────
# Config
# ──────────────────────────────
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

MAX_SIZE_MB = 48  # Safe Telegram limit

# ──────────────────────────────
# Helpers
# ──────────────────────────────
def dev_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2")]]
    )

def get_search(query: str) -> str:
    if query.startswith("http"):
        return query
    return f"ytsearch1:{query}"

def build_caption(info, user):
    size = info.get("filesize") or info.get("filesize_approx") or 0
    size_mb = round(size / 1024 / 1024, 2)

    return (
        f"🎬 *Title:* {info.get('title','N/A')}\n"
        f"📺 *Channel:* {info.get('uploader','N/A')}\n"
        f"⏰ *Duration:* {info.get('duration_string','N/A')}\n"
        f"📦 *File Size:* {size_mb} MB\n"
        f"👀 *Views:* {info.get('view_count','N/A')}\n\n"
        f"🙋 *Requested by:* {user.mention_markdown()}"
    )

# ──────────────────────────────
# Commands
# ──────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome!*\n\n"
        "🎵 `/song <name>` – Audio\n"
        "🎬 `/video <name>` – Compressed video\n\n"
        "Example:\n"
        "`/video sanam re`\n\n"
        "🚀 @deweni2",
        parse_mode="Markdown",
        reply_markup=dev_button()
    )

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ `/video <name or url>`", parse_mode="Markdown")
        return

    query = " ".join(context.args)
    search = get_search(query)

    ydl_opts = {
        "format": "bv*[filesize_approx<50M]+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4",
            }
        ],
    }

    await update.message.reply_text("🎬 Downloading & compressing...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=True)

            if "entries" in info:
                info = info["entries"][0]

            file_path = ydl.prepare_filename(info)

        size_mb = os.path.getsize(file_path) / 1024 / 1024

        if size_mb > MAX_SIZE_MB:
            os.remove(file_path)
            await update.message.reply_text(
                f"❌ Video too large after compression ({round(size_mb,2)} MB)\nTry shorter video."
            )
            return

        caption = build_caption(info, update.message.from_user)

        await update.message.reply_video(
            video=open(file_path, "rb"),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=dev_button()
        )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n`{e}`", parse_mode="Markdown")

# ──────────────────────────────
# Main
# ──────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", video))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
