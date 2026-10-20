import subprocess
from telegram import Update
from telegram.ext import Application,MessageHandler,filters,CommandHandler,ContextTypes
BOT_TOKEN="8877635317:AAEkFwmpRktG1QAAvVYEj0fxpRlUSzkXyqE"
async def start(u,c): await u.message.reply_text("Bot ON - send video")
async def handle(u,c):
 m=await u.message.reply_text("Cutting 45s...")
 try:
  vid=u.message.video or u.message.document
  f=await c.bot.get_file(vid.file_id)
  await f.download_to_drive("i.mp4")
  subprocess.run(["ffmpeg","-y","-ss","0","-t","45","-i","i.mp4","-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920","-c:v","libx264","-preset","ultrafast","-c:a","aac","o.mp4"],check=True)
  await u.message.reply_video(open("o.mp4","rb"))
  await m.delete()
 except Exception as e: await u.message.reply_text(str(e))
app=Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.VIDEO|filters.Document.VIDEO,handle))
app.run_polling()
