import os
import collections
import discord
import asyncio

global players


class Player:
    """Class for playing audio files in Discord voice channels

    Args:
        channel: Discord voice channel to connect to
        players: List of currently active players
        loop: Current asyncio event loop

    """

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
        """Callback method for when player is successfully connected to voice channel

        Returns:
            None

        """
        self.channel = future.result()
        self.check_queue()

    def clear_queue(self):
        """Clears current play queue

        Returns:
            None

        """
        self.queue.clear()

    def add_to_queue(self, cmd, *args):
        """Add command to queue. Will also automatically check queue

        Args:
            cmd: Command to add to queue

        Returns:
            None

        """
        self.queue.append((cmd, *args))
        if (
            len(self.queue) == 1
            and self.connectionTask.done()
            and not self.channel.is_playing()
        ):
            self.check_queue()

    def play_mp3(self, path):
        """Plays audio file specified by path

        Args:
            path: Path of audio file to play

        Returns:
            None

        """
        source = discord.FFmpegOpusAudio(path)
        self.channel.play(source, after=lambda e: self.check_queue())

    def check_queue(self):
        """Check current queue. If queue is empty, leaves voice channel, otherwise plays next audio file in queue

        Returns:
            None

        """
        while not self.connectionTask.done():
            continue

        if not self.channel.is_connected():
            return

        if len(self.queue) != 0:
            cmd, args = self.queue.popleft()
            self.play_mp3(f"./sound_bytes/memes/{cmd}.mp3")

        elif len(self.queue) == 0:
            self.loop.create_task(self.leave_channel())

    async def leave_channel(self):
        """Leaves current voice channel

        Returns:
            None

        """
        if self.channel.guild.name in self.players:
            await self.channel.disconnect()
            self.players.pop(self.channel.guild.name)
