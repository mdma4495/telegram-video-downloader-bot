import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "📥 Video download karne ke liye YouTube / Instagram / Facebook ka link bhejo."
    )

def is_url(text):
    url_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com|facebook\.com|fb\.watch)'
    )
    return re.match(url_regex, text)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_url(url):
        await update.message.reply_text("❌ Valid video link bhejo.")
        return

    await update.message.reply_text("⏳ Download ho raha hai, thoda wait karo...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video."):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                break

    except Exception as e:
        await update.message.reply_text("❌ Download failed. Dusra link try karo.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
