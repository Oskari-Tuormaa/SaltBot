import os
import discord
import asyncio
from dotenv import load_dotenv
from salt_client import SaltClient
from bot_debugging import run_debugging

DEBUG = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if DEBUG:
    run_debugging()
else:
    client = SaltClient()
    client.run(TOKEN)
