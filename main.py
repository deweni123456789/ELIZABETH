from pyrogram import Client
import config
from modules import adult

app = Client(
    "adult-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Register the handler with the running instance
adult.register_adult(app)

print("🤖 Adult Bot is running...")
app.run()
