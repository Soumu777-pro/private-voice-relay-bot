import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
import sounddevice as sd
import numpy as np

# --------------------------
# Environment Variables
# --------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
SESSION_STRING = os.getenv("SESSION_STRING")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID"))
RECORD_GROUP_ID = int(os.getenv("RECORD_GROUP_ID"))

# --------------------------
# Initialize clients
# --------------------------
# Bot client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Assistant client
assistant = Client("sessions/assistant_session", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# PyTgCalls for assistant
pytgcalls = PyTgCalls(assistant)

# Dynamic play group
play_group_id = None

# --------------------------
# Audio settings
# --------------------------
level = 10  # 1–20
bass = 5    # 1–10
mute = False

# --------------------------
# FFmpeg mic streaming setup
# --------------------------
RATE = 48000
CHANNELS = 2

def start_ffmpeg_process():
    cmd = [
        "ffmpeg",
        "-f", "f32le",
        "-ar", str(RATE),
        "-ac", str(CHANNELS),
        "-i", "-",
        "-af", f"volume={level}dB,bass=g={bass}",
        "-f", "s16le",
        "-"
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

ffmpeg_proc = None

def mic_callback(indata, frames, time, status):
    if not mute:
        ffmpeg_proc.stdin.write(indata.tobytes())

# --------------------------
# BOT COMMANDS
# --------------------------

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply("Bot is online ✅")

# /join command
@app.on_message(filters.command("join") & filters.user(OWNER_ID))
async def join_play(client, message: Message):
    global play_group_id, ffmpeg_proc
    if len(message.command) < 2:
        await message.reply("Usage: /join <chat_id>")
        return

    try:
        play_group_id = int(message.command[1])
        # Check assistant membership
        try:
            await assistant.get_chat_member(play_group_id, "me")
        except:
            await message.reply("⚠ Please add assistant id to Play group!")
            play_group_id = None
            return

        # Start FFmpeg process if not started
        if not ffmpeg_proc:
            ffmpeg_proc = start_ffmpeg_process()
            sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=mic_callback).start()

        # Join Record VC
        await pytgcalls.join_group_call(
            RECORD_GROUP_ID,
            InputStream(AudioPiped("-"))
        )

        # Join Play VC
        await pytgcalls.join_group_call(
            play_group_id,
            InputStream(AudioPiped("-"))
        )

        await message.reply(f"Assistant joined Record VC + Play VC ✅")

    except Exception as e:
        await message.reply(f"Error: {e}")
        play_group_id = None

# /level 1–20
@app.on_message(filters.command("level") & filters.user(OWNER_ID))
async def level_cmd(client, message: Message):
    global level
    if len(message.command) < 2:
        await message.reply(f"Current level: {level}")
        return
    try:
        lvl = int(message.command[1])
        if 1 <= lvl <= 20:
            level = lvl
            await message.reply(f"Voice level set to {level}/20 ✅")
        else:
            await message.reply("Use a level between 1 and 20")
    except:
        await message.reply("Invalid value")

# /bass 1–10
@app.on_message(filters.command("bass") & filters.user(OWNER_ID))
async def bass_cmd(client, message: Message):
    global bass
    if len(message.command) < 2:
        await message.reply(f"Current bass: {bass}")
        return
    try:
        b = int(message.command[1])
        if 1 <= b <= 10:
            bass = b
            await message.reply(f"Bass set to {bass}/10 ✅")
        else:
            await message.reply("Use bass between 1 and 10")
    except:
        await message.reply("Invalid value")

# /mute & /unmute
@app.on_message(filters.command("mute") & filters.user(OWNER_ID))
async def mute_cmd(client, message: Message):
    global mute
    mute = True
    await message.reply("Assistant muted ✅")

@app.on_message(filters.command("unmute") & filters.user(OWNER_ID))
async def unmute_cmd(client, message: Message):
    global mute
    mute = False
    await message.reply("Assistant unmuted ✅")

# /leaveplay
@app.on_message(filters.command("leaveplay") & filters.user(OWNER_ID))
async def leave_play(client, message: Message):
    global play_group_id
    if play_group_id:
        await pytgcalls.leave_group_call(play_group_id)
        await message.reply("Assistant left Play VC ✅")
        play_group_id = None
    else:
        await message.reply("No Play VC to leave!")

# /leaverecord
@app.on_message(filters.command("leaverecord") & filters.user(OWNER_ID))
async def leave_record(client, message: Message):
    await pytgcalls.leave_group_call(RECORD_GROUP_ID)
    await message.reply("Assistant left Record VC ✅")

# /screenshare placeholder
@app.on_message(filters.command("screenshare") & filters.user(OWNER_ID))
async def screenshare_cmd(client, message: Message):
    global play_group_id
    if not play_group_id:
        await message.reply("Set a play group first with /join <chat_id>")
        return
    await message.reply(f"Assistant starts screenshare in {play_group_id} ✅")
    # TODO: Implement live screen capture feed

# --------------------------
# Run Bot + Assistant
# --------------------------
async def main():
    await app.start()
    await assistant.start()
    await pytgcalls.start()
    print("Bot + Assistant running...")
    await asyncio.Event().wait()  # keep alive

if __name__ == "__main__":
    asyncio.run(main())
