import asyncio
from typing import Dict

import discord

# Dictionary mapping guild ID's to `Player` objects
ALL_PLAYERS: Dict[int, "Player"] = dict()


def get_player(guild_id: int) -> "Player":
    if guild_id not in ALL_PLAYERS:
        ALL_PLAYERS[guild_id] = Player()
    return ALL_PLAYERS[guild_id]


class Player:
    def __init__(self):
        self.vc: discord.VoiceClient = None
        self.loop = asyncio.get_running_loop()
        self.queue = []

    async def connect_to_vc(self, vc: discord.VoiceChannel):
        if self.vc and self.vc.is_connected():
            return
        self.vc = await vc.connect()

    async def disconnect(self):
        if self.vc and self.vc.is_connected():
            await self.vc.disconnect()

    async def add_to_queue(self, *params):
        self.queue += params
        if (
                len(self.queue) == len(params)
                and not self.vc.is_playing()
        ):
            await self.check_queue()

    async def check_queue(self):
        if not self.vc.is_connected():
            return

        if len(self.queue) == 0:
            await self.disconnect()
            return

        clip = self.queue.pop(0)
        self.vc.play(clip.source(), after=self.clip_done)

    def clip_done(self, e):
        task = self.loop.create_task(self.check_queue())
        asyncio.ensure_future(task)
