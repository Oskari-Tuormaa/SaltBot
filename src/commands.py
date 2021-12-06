import discord

ALL_COMMANDS = dict()


def register_command(name: str):
    def _register_command(func):
        ALL_COMMANDS[name] = func
        return func

    return _register_command


@register_command("echo")
def test(message: discord.Message):
    print(message.content)


@register_command("hello")
def hello(message: discord.Message):
    print(f"Hello there {message.author.name}!")
