import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from moviepy.editor import VideoFileClip
import whisper

BOT_TOKEN = "8877635317:AAEkFwmpRktG1QAAvVYEj0fxpRlUSzkXyqE"
model = None

def get_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 بوت 45 ثانية واجد! ابعث فيديو")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🚀 راني نخدم...")
    try:
        f = await context.bot.get_file(update.message.video.file_id if update.message.video else update.message.document.file_id)
        await f.download_to_drive("input.mp4")
        clip = VideoFileClip("input.mp4")
        result = get_model().transcribe("input.mp4", verbose=False)
        segs = result.get("segments", [])
        best, sc = 0, -1
        for seg in segs:
            s = seg["start"]
            if s+45 > clip.duration: continue
            score = sum(len(x["text"].split()) for x in segs if s <= x["start"] < s+45)
            if score > sc:
                sc=score; best=s
        if best==0 and clip.duration>45:
            best=(clip.duration-45)/2
        final = clip.subclip(best, min(best+45, clip.duration))
        final = final.resize(height=1920).crop(width=1080, height=1920, x_center=final.w/2, y_center=final.h/2)
        final.write_videofile("out.mp4", codec="libx264", audio_codec="aac", preset="ultrafast")
        await update.message.reply_video(open("out.mp4","rb"), caption="✅ واجد HD 🔥")
        await msg.delete()
        clip.close(); final.close()
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
app.run_polling()
