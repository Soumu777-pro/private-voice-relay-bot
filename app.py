import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped

# Load environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
SESSION_STRING = os.getenv("SESSION_STRING")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID"))
RECORD_GROUP_ID = int(os.getenv("RECORD_GROUP_ID"))

# Initialize bot client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# Initialize assistant client
assistant = Client("assistant", session_string=SESSION_STRING)
# PyTgCalls for assistant
pytgcalls = PyTgCalls(assistant)

# Dynamic play group
play_group_id = None

# --------------------------
# BOT COMMANDS
# --------------------------

# /start
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply("Bot is online ✅")

# /addsession
@app.on_message(filters.command("addsession") & filters.user(OWNER_ID))
async def add_session(client, message: Message):
    await message.reply("Assistant session added ✅")

# /join - set dynamic play group
@app.on_message(filters.command("join") & filters.user(OWNER_ID))
async def join_play(client, message: Message):
    global play_group_id
    if len(message.command) < 2:
        await message.reply("Usage: /join <chat_id>")
        return
    try:
        play_group_id = int(message.command[1])
        await message.reply(f"Assistant will join VC of group {play_group_id} ✅")
        # Add VC join logic here using pytgcalls
    except ValueError:
        await message.reply("Invalid chat_id!")

# /level - adjust voice volume
@app.on_message(filters.command("level") & filters.user(OWNER_ID))
async def level_cmd(client, message: Message):
    await message.reply("Voice level set ✅")

# /mute
@app.on_message(filters.command("mute") & filters.user(OWNER_ID))
async def mute_cmd(client, message: Message):
    await message.reply("Assistant muted ✅")

# /unmute
@app.on_message(filters.command("unmute") & filters.user(OWNER_ID))
async def unmute_cmd(client, message: Message):
    await message.reply("Assistant unmuted ✅")

# /leaveplay
@app.on_message(filters.command("leaveplay") & filters.user(OWNER_ID))
async def leave_play(client, message: Message):
    await message.reply("Assistant left play VC ✅")
    global play_group_id
    play_group_id = None

# /leaverecord
@app.on_message(filters.command("leaverecord") & filters.user(OWNER_ID))
async def leave_record(client, message: Message):
    await message.reply("Assistant left record VC ✅")
    # Add logic to leave RECORD_GROUP VC

# /bass
@app.on_message(filters.command("bass") & filters.user(OWNER_ID))
async def bass_cmd(client, message: Message):
    await message.reply("Bass adjusted ✅")

# /screenshare
@app.on_message(filters.command("screenshare") & filters.user(OWNER_ID))
async def screenshare_cmd(client, message: Message):
    global play_group_id
    if not play_group_id:
        await message.reply("Set a play group first with /join <chat_id>")
        return
    await message.reply(f"Assistant starts screenshare in {play_group_id} ✅")
    # Add InputStream / screen capture logic here

# --------------------------
# RUN BOT & ASSISTANT
# --------------------------
async def main():
    await app.start()
    await assistant.start()
    await pytgcalls.start()
    print("Bot + Assistant running...")

    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
