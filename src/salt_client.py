import discord
from cmd_handler import is_valid_command, execute_commands


class SaltClient(discord.Client):
    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message: discord.Message):
        if is_valid_command(message):
            await execute_commands(message)
