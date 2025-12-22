import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome!

"
        "📥 Video download karne ke liye Instagram / Facebook ka public link bhejo."
    )
    await update.message.reply_text(text)

def is_supported_url(text):
    patterns = [
        r'instagram.com',
        r'fb.watch',
        r'facebook.com'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not is_supported_url(url):
        await update.message.reply_text("❌ Sirf Instagram/Facebook links support hote hain.")
        return
    
    await update.message.reply_text("⏳ Video download ho raha hai...")
    
    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if os.path.exists(filename):
                with open(filename, 'rb') as video_file:
                    await update.message.reply_video(video=video_file)
                os.remove(filename)
            else:
                await update.message.reply_text("❌ Video file nahi mila.")
                
    except Exception as e:
        await update.message.reply_text("❌ Download fail ho gaya. Dusra link try karo.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
