import logging
import logging.handlers
from pathlib import Path

import discord

from cmd_handler import is_valid_command, execute_commands
from metadata import root_dir, get_metadata

exception_format = """event: {event}
args: {args}
message: {message}
"""


class SaltClient(discord.Client):
    async def on_ready(self):
        # Setup logging
        log_path = Path(root_dir(), get_metadata().paths.logs).resolve()
        log_path.mkdir(exist_ok=True)
        log_file = Path(log_path, "log.log")
        rot_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10e6, backupCount=5)
        logging.basicConfig(format="\n%(asctime)s - %(levelname)s\n%(message)s", handlers=[rot_handler])

        print("Bot ready!")

    async def on_message(self, message: discord.Message):
        if is_valid_command(message):
            await execute_commands(message)

    async def on_error(self, event, *args, **kwargs):
        logging.exception(exception_format.format(event=event, args=args, message=args[0].content))
