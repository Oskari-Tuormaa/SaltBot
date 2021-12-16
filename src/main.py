import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from bot_debugging import run_debugging, DebugMode
from bot_wrapper import bot_wrapper
from metadata import root_dir, get_metadata

# Setup logging
log_path = Path(root_dir(), get_metadata().paths.logs).resolve()
log_path.mkdir(exist_ok=True)
log_file = Path(log_path, "log.log")
rot_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10e6, backupCount=5)
logging.basicConfig(format="\n%(asctime)s - %(levelname)s\n%(message)s", handlers=[rot_handler], level=logging.INFO)

# Set debug mode
DEBUG = DebugMode.LIVE

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
