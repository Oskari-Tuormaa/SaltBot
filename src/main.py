import os

from dotenv import load_dotenv

from bot_debugging import run_debugging, DebugMode
from salt_client import SaltClient
from sound_handler import normalize_audio_clips

# Set debug mode
DEBUG = DebugMode.REMOTE_DEBUG

# Get tokens
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_TOKEN = os.getenv("DISCORD_DEBUG_TOKEN")

normalize_audio_clips()

if DEBUG == DebugMode.LOCAL_DEBUG:
    run_debugging()

elif DEBUG == DebugMode.REMOTE_DEBUG:
    client = SaltClient()
    client.run(DEBUG_TOKEN)

elif DEBUG == DebugMode.LIVE:
    client = SaltClient()
    client.run(TOKEN)
