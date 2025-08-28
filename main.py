from pyrogram import Client
import config
from modules.adult import adult_handler  # import the handler

app = Client(
    "adult-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# The adult_handler in adult.py uses @Client.on_message, so it's already registered

print("🤖 Adult Bot is running...")
app.run()
