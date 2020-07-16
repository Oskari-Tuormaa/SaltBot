import os
import collections
import discord
import asyncio

global players

class Player:
    channel = None
    queue = None
    connectionTask = None
    players = {}
    loop = None

    def __init__(self, channel, players, loop):
        self.connectionTask = asyncio.get_running_loop().create_task(channel.connect())
        self.connectionTask.add_done_callback(self.connected)
        asyncio.ensure_future(self.connectionTask)
        self.queue = collections.deque()
        self.players = players
        self.loop = loop

    def connected(self, future):
        #print(" " * 500, end='\r')
        #print(", ".join(self.players), end='\r')
        self.channel = future.result()
        self.check_queue()

    def clear_queue(self):
        self.queue.clear()

    def add_to_queue(self, cmd, *args):
        self.queue.append((cmd, *args))
        if len(self.queue) == 1 and self.connectionTask.done() and not self.channel.is_playing():
            self.check_queue()

    def play_mp3(self, path):
        source = discord.FFmpegOpusAudio(path)
        self.channel.play(source, after=lambda e: self.check_queue())

    def check_queue(self):
        while not self.connectionTask.done():
            continue

        if not self.channel.is_connected():
            return

        if len(self.queue) != 0:
            cmd, args = self.queue.popleft()
            self.play_mp3(f'./sound_bytes/memes/{cmd}.mp3')

        elif len(self.queue) == 0:
            self.loop.create_task(self.leave_channel())

    async def leave_channel(self):
        if self.channel.guild.name in self.players:
            await self.channel.disconnect()
            self.players.pop(self.channel.guild.name)
            #print(" " * 500, end='\r')
            #print(", ".join(self.players), end='\r')

