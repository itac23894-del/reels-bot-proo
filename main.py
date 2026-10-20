python3 -m pip install -q python-telegram-bot==20.7 --user 2>&1 | tail -n 2; python3 << 'ENDPY'
open('main.py','w').write("""import subprocess
from telegram import Update
from telegram.ext import Application,MessageHandler,filters,ContextTypes,CommandHandler
BOT_TOKEN="8877635317:AAEkFwmpRktG1QAAvVYEj0fxpRlUSzkXyqE"
async def start(u,c): await u.message.reply_text("Bot ready! Send video")
async def handle_video(u,c):
 m=await u.message.reply_text("Processing 45s...")
 try:
  vid=u.message.video or u.message.document
  f=await c.bot.get_file(vid.file_id)
  await f.download_to_drive("input.mp4")
  import json,subprocess
  r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1","input.mp4"],capture_output=True,text=True)
  dur=float(r.stdout.strip() or 0)
  st=max(0,(dur-45)/2) if dur>45 else 0
  subprocess.run(["ffmpeg","-y","-ss",str(st),"-t","45","-i","input.mp4","-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920","-c:v","libx264","-preset","ultrafast","-c:a","aac","out.mp4"],check=True)
  await u.message.reply_video(open("out.mp4","rb"),caption="Done 9:16 45s")
  await m.delete()
 except Exception as e: await u.message.reply_text(f"Err {e}")
app=Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.VIDEO|filters.Document.VIDEO,handle_video))
app.run_polling()
""")
print("main.py created")
ENDPY
