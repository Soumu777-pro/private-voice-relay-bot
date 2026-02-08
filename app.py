# app.py
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pyrogram.types import Message

API_ID = int("YOUR_API_ID")
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Initialize Pyrogram client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)

# Replace with your group IDs
RECORD_GROUP = -1001234567890
PLAY_GROUP = -1009876543210

# Example command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply("Bot is alive ✅")

# Screenshare skeleton
@app.on_message(filters.command("screenshare") & filters.group)
async def screenshare(client: Client, message: Message):
    await message.reply("Screenshare triggered! Assistant will join play VC ✅")

async def main():
    await app.start()
    await pytgcalls.start()
    print("Bot running...")
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
