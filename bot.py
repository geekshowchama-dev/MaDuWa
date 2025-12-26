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

MAX_VIDEO_MB = 48  # Telegram bot safe limit

# ──────────────────────────────
# Helpers
# ──────────────────────────────
def dev_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2")]]
    )

def search_query(q: str) -> str:
    if q.startswith("http"):
        return q
    return f"ytsearch1:{q}"

def build_caption(info, user, is_audio=False):
    size = info.get("filesize") or info.get("filesize_approx") or 0
    size_mb = round(size / 1024 / 1024, 2)

    upload_date = info.get("upload_date")
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    else:
        upload_date = "N/A"

    duration = info.get("duration")
    if duration:
        m, s = divmod(duration, 60)
        duration_str = f"{m}:{s:02d}"
    else:
        duration_str = "N/A"

    age_restricted = "Yes" if info.get("age_limit", 0) > 0 else "No"
    category = (info.get("categories") or ["N/A"])[0]

    emoji = "🎵" if is_audio else "🎬"

    return (
        f"{emoji} *Title:* {info.get('title','N/A')}\n"
        f"📺 *Channel:* {info.get('uploader','N/A')}\n"
        f"📂 *Category:* {category}\n"
        f"📅 *Upload Date:* {upload_date}\n"
        f"⏰ *Duration:* {duration_str}\n"
        f"👀 *Views:* {info.get('view_count','N/A')}\n"
        f"👍 *Likes:* {info.get('like_count','Hidden')}\n"
        f"💬 *Comments:* {info.get('comment_count','Hidden')}\n"
        f"📦 *File Size:* {size_mb} MB\n"
        f"⚖️ *License:* {info.get('license','Standard')}\n"
        f"🔞 *Age Restricted:* {age_restricted}\n\n"
        f"🙋 *Requested by:* {user.mention_markdown()}"
    )

# ──────────────────────────────
# Commands
# ──────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome!*\n\n"
        "🎵 `/song <name or url>` – Download song\n"
        "🎬 `/video <name or url>` – Download compressed video\n\n"
        "Example:\n"
        "`/song sanam re`\n"
        "`/video sanam re`\n\n"
        "🚀 Developer: @deweni2",
        parse_mode="Markdown",
        reply_markup=dev_button()
    )

# ───────────── SONG ─────────────
async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ `/song <name or url>`", parse_mode="Markdown")
        return

    query = search_query(" ".join(context.args))

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    service_msg = await update.message.reply_text("🎧 Downloading song...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if "entries" in info:
                info = info["entries"][0]
            file_path = ydl.prepare_filename(info)

        caption = build_caption(info, update.message.from_user, is_audio=True)

        await update.message.reply_audio(
            audio=open(file_path, "rb"),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=dev_button()
        )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n`{e}`", parse_mode="Markdown")

    finally:
        try:
            await service_msg.delete()
        except:
            pass

# ───────────── VIDEO ─────────────
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ `/video <name or url>`", parse_mode="Markdown")
        return

    query = search_query(" ".join(context.args))

    ydl_opts = {
        "format": "best[ext=mp4][filesize_approx<50M]/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    service_msg = await update.message.reply_text("🎬 Downloading video...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if "entries" in info:
                info = info["entries"][0]
            file_path = ydl.prepare_filename(info)

        size_mb = os.path.getsize(file_path) / 1024 / 1024
        if size_mb > MAX_VIDEO_MB:
            os.remove(file_path)
            await update.message.reply_text(
                f"❌ Video too large ({round(size_mb,2)} MB)"
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

    finally:
        try:
            await service_msg.delete()
        except:
            pass

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
