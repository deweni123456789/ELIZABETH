# modules/adult.py
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# Ensure downloads folder exists
os.makedirs('downloads', exist_ok=True)

# yt-dlp options
YDL_OPTS = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,  # For Railway SSL issues
}

async def download_video(url: str):
    loop = asyncio.get_event_loop()
    info = {}

    def run_ydl():
        nonlocal info
        try:
            with YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(url, download=True)
        except Exception as e:
            raise RuntimeError(f"yt-dlp error: {e}")

    await loop.run_in_executor(None, run_ydl)
    filename = YDL_OPTS['outtmpl'] % {'title': info['title'], 'ext': info.get('ext', 'mp4')}
    return filename, info

@Client.on_message(filters.private & filters.command("adult"))
async def adult_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a video link:\n/adult <link>")
        return

    url = message.command[1]
    msg = await message.reply_text("⏳ Downloading your video...")

    try:
        file_path, info = await download_video(url)
    except Exception as e:
        await msg.edit(f"❌ Failed to download video:\n{e}")
        print(f"[ERROR] Download failed: {e}")
        return

    caption = (
        f"**Title:** {info.get('title', 'N/A')}\n"
        f"**Channel:** {info.get('uploader', 'N/A')}\n"
        f"**Views:** {info.get('view_count', 'N/A')}\n"
        f"**Likes:** {info.get('like_count', 'N/A')}\n"
        f"**Dislikes:** {info.get('dislike_count', 'N/A')}\n"
        f"**Comments:** {info.get('comment_count', 'N/A')}\n"
        f"**Requested by:** {message.from_user.mention}"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Developer", url="https://t.me/deweni2")]]
    )

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption,
            reply_markup=buttons,
            supports_streaming=True
        )
    except Exception as e:
        await msg.edit(f"❌ Failed to upload video:\n{e}")
        print(f"[ERROR] Upload failed: {e}")
        return

    await msg.delete()
    # Clean up downloaded file
    if os.path.exists(file_path):
        os.remove(file_path)
