import discord
from commands import ALL_COMMANDS


def is_valid_command(message: discord.Message) -> bool:
    """ Checks if message should be ignored or not. """
    return message.content.strip().startswith("!") and not message.author.bot


async def execute_commands(message: discord.Message):
    """ Execute all commands in message. """
    cmd, *params = message.content.strip()[1:].split()
    await ALL_COMMANDS[cmd](message, *params)
