import os
import re
import yt_dlp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔴 YAHAN APNA BOT TOKEN DAALO (recommended)
BOT_TOKEN = os.getenv("BOT_TOKEN") or "PASTE_YOUR_BOT_TOKEN_HERE"


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "🎥 Instagram ya Facebook ka *public video link* bhejo\n"
        "📥 Video download karke bhej diya jayega",
        parse_mode="Markdown"
    )


# URL validation
def is_valid_url(text: str) -> bool:
    pattern = r"(https?://)?(www\.)?(instagram\.com|facebook\.com|fb\.watch)/.+"
    return re.search(pattern, text) is not None


# Video download handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    if not is_valid_url(url):
        await update.message.reply_text(
            "❌ Sirf *Instagram ya Facebook* ka public link bhejo",
            parse_mode="Markdown"
        )
        return

    chat_id = update.message.chat_id
    filename = f"video_{chat_id}.mp4"

    await update.message.reply_text("⏳ Download ho raha hai, please wait...")

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(filename):
            await update.message.reply_text("❌ Video download nahi ho paya")
            return

        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ Video downloaded successfully"
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error aaya:\n`{str(e)}`",
            parse_mode="Markdown"
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
