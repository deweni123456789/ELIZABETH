from pyrogram import Client
import config
import modules.adult  # just import to register handler

app = Client(
    "adult-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

print("🤖 Adult Bot is running...")
app.run()
