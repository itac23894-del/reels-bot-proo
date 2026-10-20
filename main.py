import os, subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = "8877635317:AAEkFwmpRktG1QAAvVYEj0fxpRlUSzkXyqE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 بوت 45 ثانية واجد! ابعث فيديو طويل، نرجعو 9:16 HD")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🚀 نقطعو 45 ثانية من الوسط...")
    try:
        vid = update.message.video or update.message.document
        f = await context.bot.get_file(vid.file_id)
        await f.download_to_drive("input.mp4")
        
        # نجيب المدة
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1","input.mp4"], capture_output=True, text=True)
        duration = float(r.stdout.strip() or 0)
        start = max(0, (duration - 45) / 2) if duration > 45 else 0
        
        # نقص 45 ثانية + نحول ل 9:16
        cmd = [
            "ffmpeg","-y","-ss",str(start),"-t","45","-i","input.mp4",
            "-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v","libx264","-preset","ultrafast","-crf","23","-c:a","aac","-b:a","128k",
            "out.mp4"
        ]
        subprocess.run(cmd, check=True)
        
        await update.message.reply_video(open("out.mp4","rb"), caption="✅ واجد! 45s - 1080x1920")
        await msg.delete()
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
app.run_polling()
