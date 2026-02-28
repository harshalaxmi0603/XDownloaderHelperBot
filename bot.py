import os
import threading
from flask import Flask
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------- Telegram Bot --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send a video link")
        return

    url = context.args[0]
    await update.message.reply_text("⬇️ Downloading...")

    filename = "video.mp4"

    with yt_dlp.YoutubeDL({"outtmpl": filename, "format": "best"}) as ydl:
        ydl.download([url])

    await update.message.reply_video(video=open(filename, "rb"))
    os.remove(filename)

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


# -------- Fake Web Server (for Render FREE) --------
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot running"


if __name__ == "__main__":
    threading.Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)
