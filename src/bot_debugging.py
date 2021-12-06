import discord
from salt_client import SaltClient
import asyncio
import enum


class DebugMode(enum.Enum):
    LOCAL_DEBUG = 1
    REMOTE_DEBUG = 2
    LIVE = 3


class DummyChannel:
    def __init__(self):
        ...

    async def send(self, mes: str):
        print(mes)


class DummyUser:
    def __init__(self, name="", bot=False):
        self.name = name
        self.bot = bot


class DummyMessage:
    def __init__(self, content="", author=DummyUser(), channel=DummyChannel()):
        self.content = content
        self.author = author
        self.channel = channel


def run_debugging():
    """ Runs various debugging commands. """
    client = SaltClient()
    messages = [
        DummyMessage("!asciimath sqrt(2)"),
    ]

    asyncio.run(client.on_ready())

    for message in messages:
        asyncio.run(client.on_message(message))
