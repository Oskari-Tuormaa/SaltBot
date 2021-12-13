import os

from dotenv import load_dotenv

from bot_debugging import run_debugging, DebugMode
from bot_wrapper import bot_wrapper

# Set debug mode
DEBUG = DebugMode.REMOTE_DEBUG

# Get tokens
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_TOKEN = os.getenv("DISCORD_DEBUG_TOKEN")

if DEBUG == DebugMode.LOCAL_DEBUG:
    run_debugging()

elif DEBUG == DebugMode.REMOTE_DEBUG:
    bot_wrapper(DEBUG_TOKEN)

elif DEBUG == DebugMode.LIVE:
    bot_wrapper(TOKEN)
