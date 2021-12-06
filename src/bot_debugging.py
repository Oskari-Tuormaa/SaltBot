import discord
from salt_client import SaltClient
import asyncio


class DummyUser:
    def __init__(self, name="", bot=False):
        self.name = name
        self.bot = bot


class DummyMessage:
    def __init__(self, content="", author=DummyUser()):
        self.content = content
        self.author = author


def run_debugging():
    """ Runs various debugging commands. """
    client = SaltClient()
    messages = [
        DummyMessage("Test!"),
        DummyMessage("!echo hello", DummyUser(name="Yee")),
    ]

    asyncio.run(client.on_ready())

    for message in messages:
        asyncio.run(client.on_message(message))
