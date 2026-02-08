# private-voice-relay-bot
# Private Voice Relay Bot

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Soumu777-pro/private-voice-relay-bot&env[API_ID]=&env[API_HASH]=&env[BOT_TOKEN]=&env[OWNER_ID]=&env[SESSION_STRING]=&env[RECORD_GROUP_ID]=)

A private Telegram voice relay bot to relay your voice from a **logger/record group** to a **play group** in real-time.  
Supports **volume control**, **bass adjustment**, and optional **screenshare**.

This bot is intended for **personal use** only.

---

## ⚡ Features

- Join **record VC** silently (assistant ID)
- Relay voice to **play VC** live
- `/level 1-20` → Adjust voice volume
- `/bass 1-10` → Optional bass boost
- `/mute` & `/unmute` assistant
- Dynamic **/join <chat_id>** command to select play group
- Optional **/screenshare** command

---

## 🛠️ Requirements

- Python 3.10+
- Heroku (or Linux server)
- FFmpeg installed (via buildpack on Heroku)

**Dependencies** are listed in [`requirements.txt`](requirements.txt).

---

## ⚙️ Setup

1. **Clone the repo**
```bash
git clone https://github.com/Soumu777-pro/private-voice-relay-bot.git
cd private-voice-relay-bot
