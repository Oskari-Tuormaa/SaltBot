import os
import math
import discord
import random
from player import Player

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
        if IS_DEBUGGING:
            await self.change_presence(
                status=discord.Status.dnd, activity=discord.Game("absolutely nothing")
            )
        else:
            await self.change_presence(
                status=discord.Status.online,
                activity=discord.Game("with piles of salt"),
            )
        await self.check_new_mp3s()

        print("Ready!")

    async def check_new_mp3s(self):
        files_in_raw = set(
            filter(lambda x: x.endswith(".mp3"), os.listdir("sound_bytes/memes_raw"))
        )
        files_in_norm = set(
            filter(lambda x: x.endswith(".mp3"), os.listdir("sound_bytes/memes"))
        )

        # If there's a difference between raw and normalized
        if len(files_in_norm.symmetric_difference(files_in_raw)) != 0:
            new_com = [x for x in files_in_raw.difference(files_in_norm)]
            old_com = [x for x in files_in_norm.difference(files_in_raw)]

            # Remove all normalized mp3s
            for f in old_com:
                f_path = os.path.join("sound_bytes/memes", f)
                os.remove(f_path)

            # Run normalization
            os.system(f"sound_bytes/normalize_memes.sh {' '.join(new_com)}")

            # Update saltbot-help channels
            for guild in self.guilds:
                for channel in guild.channels:
                    if channel.name == "saltbot-help":
                        await channel.purge()
                        if len(new_com) != 0:
                            new_com_embed = discord.Embed(
                                title="New commands:",
                                description=", ".join([x[:-4] for x in new_com]),
                                colour=discord.Colour.gold(),
                            )
                            await channel.send(embed=new_com_embed)
                        if len(old_com) != 0:
                            old_com_embed = discord.Embed(
                                title="Commands deleted:",
                                description=", ".join([x[:-4] for x in old_com]),
                                colour=discord.Colour.red(),
                            )
                            await channel.send(old_com_embed)
                        await self.print_help(channel)

    async def on_message(self, message):
        if (
            (len(message.content) != 0)
            and (
                message.content[0] == "!"
                or (
                    message.channel.name == "saltbot-help"
                    and message.content not in ["help", "!help"]
                )
            )
            and not message.author.bot
        ):
            if IS_DEBUGGING and message.guild.name != "Min Test Server":
                await message.channel.send(
                    "Sorry my dude, I'm currently under construction, I'll hopefully be back in a jiffy"
                )
                return

            if message.channel.name == "saltbot-help":
                message.content = "!" + message.content

            # Check for sneaky
            cmds = message.content[1:].split(" ")
            if "-sneaky" in cmds:
                cmds.remove("-sneaky")
                await message.delete()

            await self.dispatcher(cmds, message)

        if message.channel.name == "saltbot-help" and message.author != self.user:
            await message.delete()

    async def print_help(self, channel):
        files = os.listdir("./sound_bytes/memes")
        files = [x[:-4] for x in files if x[-4:] == ".mp3"]
        files.sort()
        command_mes = discord.Embed(
            title="Commands:",
            description="!help - Shows this help message\n!skrid - Disconnects SaltBot from voice channel\n!leave - Disconnects SaltBot from voice channel",
        )
        await channel.send(embed=command_mes)
        voice_command_mes = discord.Embed(title="Voice commands:", description="")

        num_col = 3
        num_row = math.ceil(len(files) / num_col)
        per = (int)(len(files) / num_col)
        cols = []
        temp_point = 0
        for i in range(num_col):
            col_len = per if i >= (len(files) % num_col) else per + 1
            cols.append(files[temp_point : temp_point + col_len])
            temp_point += col_len

        voice_command_mes.description += "```\n"
        for i in range(num_row):
            mes = ""
            for j in range(num_col):
                if j != num_col - 1:
                    mes += cols[j][i].ljust(20, " ")
                else:
                    mes += cols[j][i]
            voice_command_mes.description += mes + "\n"
        voice_command_mes.description += "```"

        await channel.send(embed=voice_command_mes)

    async def dispatcher(self, cmds, message):
        for cmd in cmds:
            if os.path.isfile(f"./sound_bytes/memes/{cmd}.mp3"):
                if message.author.voice == None:
                    # await message.channel.send("You're not in a channel")
                    return

                if (
                    message.guild.name not in players
                    or players[message.guild.name] == None
                ):
                    players[message.guild.name] = Player(
                        message.author.voice.channel, players, self.loop
                    )

                players[message.guild.name].add_to_queue(cmd, None)

            elif cmd == "help":
                await self.print_help(message.channel)

            elif cmd == "skrid" or cmd == "leave":
                if message.guild.name in players:
                    await players[message.guild.name].channel.disconnect()
                    players[message.guild.name].clear_queue()
                    players.pop(message.guild.name)
                else:
                    await message.channel.send("I'm not even in a channel")

            # else:
            #     await message.channel.send(
            #         "{}: {}".format(cmd, random.choice(UNKNOWN_CMD))
            #     )
