import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Instagram video downloader bot!

Instagram reel/post link bhejo.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if 'instagram.com' not in url:
        await update.message.reply_text("❌ Sirf Instagram link bhejo!")
        return
    
    await update.message.reply_text("⏳ Download ho raha hai...")
    
    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': 'video.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video_file:
            await update.message.reply_video(video=video_file)
        
        os.remove('video.mp4')
        
    except:
        await update.message.reply_text("❌ Download fail. Public Instagram link try karo.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
