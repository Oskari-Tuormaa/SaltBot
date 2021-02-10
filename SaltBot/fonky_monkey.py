import datetime
import asyncio
import threading


class FonkyMonkey:
    guilds = []
    check_delay = 10
    has_sent = False
    fonky_url = "https://www.youtube.com/watch?v=nxoe5DjDd74"

    def __init__(self, guilds, loop: asyncio.SelectorEventLoop):
        self.guilds = guilds
        self.loop = loop

        thread = threading.Thread(target=self.startup, args=(self.loop,))
        thread.start()

    def startup(self, loop: asyncio.SelectorEventLoop):
        asyncio.set_event_loop(loop)
        loop.create_task(self.sleep_then_check())

    async def sleep_then_check(self):
        await self.initial_check()
        await self.check()
        while True:
            await asyncio.sleep(self.check_delay)
            await self.check()

    async def initial_check(self):
        for guild in self.guilds:
            channel = guild.text_channels[0]
            dt = datetime.datetime.now()
            dt = dt.replace(hour=0, minute=0, second=0)
            async for message in channel.history(after=dt):
                if message.author.bot and message.content == self.fonky_url:
                    self.has_sent = True
                    break
            if self.has_sent == True:
                break

    async def check(self):
        dt = datetime.datetime.today()

        if self.has_sent:
            if dt.weekday() == 0:  # If monday
                self.has_sent = False
        else:
            if dt.weekday() == 4 and dt.hour > 12:  # Friday past 12
                await self.send_fonky()
                self.has_sent = True

    async def send_fonky(self):
        for guild in self.guilds:

            await guild.text_channels[0].send(self.fonky_url)
