import discord
from commands import ALL_COMMANDS
from sound_handler import is_sound_command, play_sound_commands


def is_valid_command(message: discord.Message) -> bool:
    """ Checks if message should be ignored or not. """
    return message.content.strip().startswith("!") and not message.author.bot


async def execute_commands(message: discord.Message):
    """ Execute all commands in message. """
    cmd, *params = message.content.strip()[1:].split()

    # Prefer sound commands
    if is_sound_command(cmd):
        await play_sound_commands(message, cmd, *params)
        return

    if cmd in ALL_COMMANDS:
        await ALL_COMMANDS[cmd](message, *params)
