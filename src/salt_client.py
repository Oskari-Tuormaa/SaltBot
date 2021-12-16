import logging
import logging.handlers

import discord

from cmd_handler import is_valid_command, execute_commands

exception_format = """event: {event}
args: {args}
message: {message}
"""


class SaltClient(discord.Client):
    async def on_ready(self):
        print("Bot ready!")

    async def on_message(self, message: discord.Message):
        if is_valid_command(message):
            await execute_commands(message)

    async def on_error(self, event, *args, **kwargs):
        logging.exception(exception_format.format(event=event, args=args, message=args[0].content))
