import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send a video link")
        return

    url = context.args[0]

    await update.message.reply_text("⬇️ Downloading...")

    filename = "video.mp4"

    ydl_opts = {
        "outtmpl": filename,
        "format": "best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open(filename, "rb"))
        os.remove(filename)

    except:
        await update.message.reply_text("❌ Failed to download")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running...")
app.run_polling()