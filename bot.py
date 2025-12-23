import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Welcome!

📥 Video download karne ke liye Instagram / Facebook ka public link bhejo."
    await update.message.reply_text(text)


def is_url(text: str) -> bool:
    pattern = r"^(https?://)?(www.)?(instagram.com|facebook.com|fb.watch)"
    return re.match(pattern, text) is not None


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    if not is_url(url):
        await update.message.reply_text("❌ Sirf Instagram / Facebook ka valid public video link bhejo.")
        return

    await update.message.reply_text("⏳ Download ho raha hai, thoda wait karo...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file_name in os.listdir():
            if file_name.startswith("video."):
                with open(file_name, "rb") as f:
                    await update.message.reply_video(video=f)
                os.remove(file_name)
                break

    except Exception as e:
        print("Download error:", e)
        await update.message.reply_text("❌ Download failed. Public Insta/Facebook link try karo.")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable set nahi hai.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
