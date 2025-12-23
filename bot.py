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

BOT_TOKEN = os.environ.get("BOT_TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome!\n\n"
        "🎥 Video download karne ke liye\n"
        "Instagram ya Facebook ka public link bhejo"
    )
    await update.message.reply_text(text)


# URL check
def is_valid_url(text: str) -> bool:
    pattern = r"(https?://)?(www\.)?(instagram\.com|facebook\.com|fb\.watch)/.+"
    return re.match(pattern, text) is not None


# Video download handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    if not is_valid_url(url):
        await update.message.reply_text(
            "❌ Sirf Instagram ya Facebook ka public link bhejo"
        )
        return

    await update.message.reply_text("⏳ Download ho raha hai, thoda wait karo...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # downloaded file find karo
        filename = None
        for file in os.listdir("."):
            if file.startswith("video."):
                filename = file
                break

        if not filename:
            await update.message.reply_text("❌ Video download nahi ho paya")
            return

        await update.message.reply_video(video=open(filename, "rb"))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ Error aaya, video download nahi ho saka")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()


if __name__ == "__main__":
    main()
