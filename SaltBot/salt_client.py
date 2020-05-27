import os
import discord
import random
from player import Player

players = {}

UNKNOWN_CMD = [ "Kæmpe spurgt", "Wat?", "A hva?", "Den skal jeg sgu lige have igen", "Jaj ik fostå" ]

class SaltClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game("with piles of salt"))
        print("Ready!")

    async def on_message(self, message):
        if (message.content[0] == '!'):
            cmd = message.content[1:]
            await self.dispatcher(cmd, message)
            
    async def dispatcher(self, cmd, message):
        if os.path.isfile(f'./sound_bytes/memes/{cmd}.mp3'):
            if message.author.voice == None:
                await message.channel.send("You're not in a channel")
                return

            if message.guild.name not in players or players[message.guild.name] == None:
                players[message.guild.name] = Player(message.author.voice.channel, players, self.loop)

            players[message.guild.name].add_to_queue(cmd, None)

        elif cmd == "help":
            await message.channel.send("{} is a big dumb baby".format(message.author.name))

        elif cmd == "skrid":
            if message.guild.name in players:
                print(" " * 500, end='\r')
                print(players, end='\r')
                await players[message.guild.name].channel.disconnect()
            else:
                await message.channel.send("I'm not even in a channel")


        else:
            await message.channel.send(random.choice(UNKNOWN_CMD))
