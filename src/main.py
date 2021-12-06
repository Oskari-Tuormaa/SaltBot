import os
import discord
import asyncio
from dotenv import load_dotenv
from salt_client import SaltClient
from bot_debugging import run_debugging, DebugMode

DEBUG = DebugMode.REMOTE_DEBUG

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_TOKEN = os.getenv("DISCORD_DEBUG_TOKEN")

if DEBUG == DebugMode.LOCAL_DEBUG:
    run_debugging()
elif DEBUG == DebugMode.REMOTE_DEBUG:
    client = SaltClient()
    client.run(DEBUG_TOKEN)
elif DEBUG == DebugMode.LIVE:
    client = SaltClient()
    client.run(TOKEN)
