import os
import math
import discord
import random
from player import Player
from fonky_monkey import FonkyMonkey

from typing import List

players = {}

IS_DEBUGGING = False

UNKNOWN_CMD = [
    "Kæmpe spurgt",
    "Wat?",
    "A hva?",
    "Den skal jeg sgu lige have igen",
    "Jaj ik fostå",
]


class SaltClient(discord.Client):
    async def on_ready(self):
        """ Called when bot is initialized """

        # Set presence
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("with piles of salt"),
        )

        # Check changes in mp3s
        await self.check_new_mp3s()

        # Start FonkyMonkey routine
        self.fonky_monkey = FonkyMonkey(self.guilds, self.loop)

        print("Ready!")

    async def check_new_mp3s(self):
        """Checks for new sound bytes and updates saltbot-help channels in each guild

        Returns:
            None

        """
        # Get sets with all mp3s in raw and normalized directories
        files_in_raw = set(
            filter(lambda x: x.endswith(".mp3"), os.listdir("sound_bytes/memes_raw"))
        )
        files_in_norm = set(
            filter(lambda x: x.endswith(".mp3"), os.listdir("sound_bytes/memes"))
        )

        new_com = []
        old_com = []
        # If there's a difference between raw and normalized
        if len(files_in_norm.symmetric_difference(files_in_raw)) != 0:
            # Get unique files in each directory
            new_com = [x for x in files_in_raw.difference(files_in_norm)]
            old_com = [x for x in files_in_norm.difference(files_in_raw)]

            # Remove all normalized mp3s
            for f in old_com:
                f_path = os.path.join("sound_bytes/memes", f)
                os.remove(f_path)

            # Run normalization
            if len(new_com) != 0:
                os.system(f"sound_bytes/normalize_memes.sh {' '.join(new_com)}")

        # Update saltbot-help channels
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == "saltbot-help":
                    # Remove all messages in channel
                    await channel.purge()

                    # If there are new commands
                    if len(new_com) != 0:
                        new_com_embed = discord.Embed(
                            title="New commands:",
                            description=", ".join([x[:-4] for x in new_com]),
                            colour=discord.Colour.gold(),
                        )
                        await channel.send(embed=new_com_embed)
                    # If there are commands that no longer exist
                    if len(old_com) != 0:
                        old_com_embed = discord.Embed(
                            title="Commands deleted:",
                            description=", ".join([x[:-4] for x in old_com]),
                            colour=discord.Colour.red(),
                        )
                        await channel.send(embed=old_com_embed)

                    # Send help message
                    await self.print_help(channel)

    async def on_message(self, message: discord.Message):
        """ Called when message is sent in any channel """

        # If message was not sent by bot, and message is not empty
        if len(message.content) != 0 and not message.author.bot:
            # Strip message of leading and trailing whitespace
            message.content = message.content.strip()

            # Parse commands
            await self.parse_command(message)

        # If message was sent in help channel, and not by this bot, delete the message
        if message.channel.name == "saltbot-help" and message.author != self.user:
            await message.delete()

    async def parse_command(self, message: discord.Message):
        """Parses commands in message and calls dispatcher

        Args:
            message: Message containing commands to parse

        Returns:
            None

        """

        # If message was sent in saltbot channel, append !
        if message.channel.name == "saltbot-help" and not message.content.startswith(
            "!"
        ):
            message.content = "!" + message.content
            
        if message.content[0] != "!":
            return

        # Split message into commands
        cmds = message.content[1:].split(" ")

        # Delete message if -sneaky
        if "-sneaky" in cmds:
            cmds.remove("-sneaky")
            await message.delete()

        # Call dispatcher
        await self.dispatcher(cmds, message)

    async def print_help(self, channel: discord.TextChannel):
        """Prints help message in channel

        Args:
            channel: Channel to send help message to

        Returns:
            None

        """

        # Get all files in sound bytes directory
        files = os.listdir("./sound_bytes/memes")

        # Filter out non mp3 files, and remove .mp3 from names
        files = [x[:-4] for x in files if x[-4:] == ".mp3"]
        files.sort()  # Sort for alphabetical order

        # Create and send commands embed
        command_mes = discord.Embed(
            title="Commands:",
            description="!help - Shows this help message\n!skrid - Disconnects SaltBot from voice channel\n!leave - Disconnects SaltBot from voice channel",
        )
        await channel.send(embed=command_mes)

        # Create voice commands embed
        voice_command_mes = discord.Embed(title="Voice commands:", description="")

        # Set and calculate numbers for voice commands table
        num_col = 2
        num_row = math.ceil(len(files) / num_col)
        per = (int)(len(files) / num_col)

        # Create voice commands table
        cols = []
        temp_point = 0
        for i in range(num_col):
            col_len = per if i >= (len(files) % num_col) else per + 1
            cols.append(files[temp_point : temp_point + col_len])
            temp_point += col_len

        # Add voice commands table to embed
        voice_command_mes.description += "```\n"
        for i in range(num_row):
            mes = ""
            for j in range(num_col if i != num_row - 1 else len(files) % num_col):
                if j != num_col - 1:
                    mes += cols[j][i].ljust(20, " ")
                else:
                    mes += cols[j][i]
            voice_command_mes.description += mes + "\n"
        voice_command_mes.description += "```"

        # Send voice commands embed
        await channel.send(embed=voice_command_mes)

    async def dispatcher(self, cmds: List[str], message: discord.Message):
        """Sequentially executes each command in cmds

        Args:
            cmds: List of commands to execute
            message: Message from which commands are received

        Returns:
            None

        """

        # Loop through commands
        for cmd in cmds:
            # If command matches soundbyte filename
            if os.path.isfile(f"./sound_bytes/memes/{cmd}.mp3"):
                if message.author.voice == None:
                    # await message.channel.send("You're not in a channel")
                    return

                # Create player if none exists for guild
                if (
                    message.guild.name not in players
                    or players[message.guild.name] == None
                ):
                    players[message.guild.name] = Player(
                        message.author.voice.channel, players, self.loop
                    )

                # Add this soundbyte to the current queue
                players[message.guild.name].add_to_queue(cmd, None)

            elif cmd == "help":
                await self.print_help(message.channel)

            elif cmd == "skrid" or cmd == "leave":
                if message.guild.name in players:
                    await players[message.guild.name].channel.disconnect()
                    players[message.guild.name].clear_queue()
                    players.pop(message.guild.name)
                else:
                    ...
                    # await message.channel.send("I'm not even in a channel")

            # else:
            #     await message.channel.send(
            #         "{}: {}".format(cmd, random.choice(UNKNOWN_CMD))
            #     )
