from telethon import TelegramClient, events, functions, types, errors 
from telethon.tl.types import Channel, Chat, User
from dotenv import load_dotenv
import subprocess, os, asyncio, re

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))

APP_ID = os.getenv('private_app_id')
APP_HASH = os.getenv('private_app_hash')
TG_BOT_TOKEN = os.getenv('tg_aibot_token')
TG_BOT_SESSION = os.getenv('tg_aibot_session')
TG_USER_ID = os.getenv('tg_user_id')
AI_PATH = os.getenv('ai_path')

client = TelegramClient(TG_BOT_SESSION, APP_ID, APP_HASH)

@client.on(events.NewMessage(from_users=int(TG_USER_ID)))
async def start(event):
    prompt = re.sub(r"""["]""", "'", event.message.text)
    command = ["python", AI_PATH, prompt]
    answer = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    message = await client.send_message(int(TG_USER_ID), answer)

async def main():
    await client.start(bot_token=TG_BOT_TOKEN)
    await client.run_until_disconnected()
asyncio.run(main())

