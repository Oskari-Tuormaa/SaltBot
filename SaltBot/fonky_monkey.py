import discord
import datetime
import asyncio
import threading


class FonkyMonkey:
    """Class for handling posting a very fonky link each friday

    Args:
        guilds: List of guilds to post the link to
        loop: Current asyncio event loop

    """

    guilds = []
    check_delay = 10
    has_sent = False
    fonky_path = "videos/fonkymonkey.mp4"

    def __init__(self, guilds, loop: asyncio.SelectorEventLoop):
        self.guilds = guilds
        self.loop = loop

        thread = threading.Thread(target=self.startup, args=(self.loop,))
        thread.start()

    def startup(self, loop: asyncio.SelectorEventLoop):
        """Sets the current event loop and creates parallel task

        Args:
            loop: Current asyncio event loop

        Returns:
            None

        """
        asyncio.set_event_loop(loop)
        loop.create_task(self.sleep_then_check())

    async def sleep_then_check(self):
        """Sleeps for the specified amount of time before calling self.check in an infinite loop

        Returns:
            None

        """
        await self.initial_check()
        await self.check()
        while True:
            await asyncio.sleep(self.check_delay)
            await self.check()

    async def initial_check(self):
        """Does an initial check of whether this bot has posted the fonky link today

        Returns:
            None

        """
        dt = datetime.datetime.now()
        dt = dt.replace(hour=0, minute=0, second=0)
        for guild in self.guilds:
            for channel in guild.text_channels:
                async for message in channel.history(after=dt):
                    if message.author.bot:
                        for attachment in message.attachments:
                            if attachment.filename == "videos_fonkymonkey.mp4":
                                self.has_sent = True
                                return

    async def check(self):
        """Checks whether the fonky link should be posted or not

        Returns:
            None

        """
        dt = datetime.datetime.today()

        if self.has_sent:
            if dt.weekday() == 0:  # If monday
                self.has_sent = False
        else:
            if dt.weekday() == 4 and dt.hour >= 12:  # Friday past 12
                await self.send_fonky()
                self.has_sent = True

    async def send_fonky(self):
        """Sends the fonky link to the first channel in each guild

        Returns:
            None

        """
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == "saltbot-help":
                    continue
                with open(self.fonky_path, "rb") as fd:
                    fonk = discord.File(fd)
                    await channel.send(file=fonk)
                    break
