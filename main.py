from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

API_URL = "https://your-render-url.onrender.com/m3u8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Send me a YouTube Live URL and I'll grab the M3U8 link!")

async def grab_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        return await update.message.reply_text("⚠️ Please send a valid YouTube Live URL.")
    try:
        r = requests.get(API_URL, params={"url": url})
        data = r.json()
        if "m3u8_links" in data:
            reply = "\n".join([f"🔗 {link}" for link in data["m3u8_links"]])
        else:
            reply = "❌ Failed to extract the M3U8 link. Maybe it's not a live stream."
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("🚫 An error occurred. Try again later.")

app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, grab_link))

app.run_polling()
