import asyncio
import enum

from salt_client import SaltClient


class DebugMode(enum.Enum):
    LOCAL_DEBUG = 1
    REMOTE_DEBUG = 2
    LIVE = 3


class DummyTextChannel:
    async def send(self, mes: str):
        print(mes)


class DummyVoiceClient:
    def __init__(self):
        self.connected = True

    def is_connected(self):
        return self.connected

    def is_playing(self):
        return False

    async def disconnect(self):
        print("Disconnecting!")
        self.connected = False

    def play(self, clip, after=None):
        print("Playing", clip)
        if after:
            after(None)


class DummyVoiceChannel:
    async def connect(self):
        print("Connecting to voice channel!")
        return DummyVoiceClient()


class DummyVoiceState:
    def __init__(self, channel=DummyVoiceChannel()):
        self.channel = channel


class DummyUser:
    def __init__(self, name="", bot=False, voice=DummyVoiceState()):
        self.name = name
        self.bot = bot
        self.voice = voice


class DummyGuild:
    def __init__(self, id=0):
        self.id = id


class DummyMessage:
    def __init__(self, content="",
                 author=DummyUser(),
                 channel=DummyTextChannel(),
                 guild=DummyGuild()):
        self.content = content
        self.author = author
        self.channel = channel
        self.guild = guild


def run_debugging():
    """ Runs various debugging commands. """
    client = SaltClient()
    messages = [
        DummyMessage("!askdjalsd")
    ]

    asyncio.run(client.on_ready())

    for message in messages:
        asyncio.run(client.on_message(message))
