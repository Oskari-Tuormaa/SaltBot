import discord
import sympy as sp
import re

ALL_COMMANDS = dict()


def register_command(name: str):
    """ Registers command to command dict. """

    def _register_command(func):
        ALL_COMMANDS[name] = func
        return func

    return _register_command


@register_command("whatis")
async def whatis(message: discord.Message, target: str):
    """`whatis [cmd]`

    Prints docstring for [cmd]."""
    if target in ALL_COMMANDS:
        doc = ALL_COMMANDS[target].__doc__
        if doc is not None:
            await message.channel.send(doc)
        else:
            await message.channel.send("```Command doesn't have docstring.```")


@register_command("commands")
async def commands(message: discord.Message):
    """`commands`

    Lists all commands."""
    mes = "```"
    for k in ALL_COMMANDS.keys():
        mes += k + "\n"
    mes += "```"
    await message.channel.send(mes)


@register_command("test")
async def test(message: discord.Message):
    """`test`

    Simply writes "Test" in channel."""
    print("Test")


@register_command("echo")
async def echo(message: discord.Message, params: str = "Nothing to echo :/"):
    """`echo [message]`

    Echoes the message specified by [message]."""
    await message.channel.send(params)


@register_command("hello")
async def hello(message: discord.Message):
    """`hello`

    Greets user."""
    await message.channel.send(f"Hello {message.author.name}!")


@register_command("purge")
async def purge_channel(message: discord.Message):
    """`purge`

    > Deletes all messages in channel."""
    await message.channel.purge()


@register_command("asciimath")
async def asciimath(message: discord.Message, *expr):
    """`asciimath [expr]`

    Evaluates [expr] using Sympy."""
    expr = " ".join(expr)
    words = set(re.findall(r"[^\d\s\(\)+*/\-,]+", expr))

    for word in words:
        if word.startswith("'"):
            expr = expr.replace(word, f"sp.symbols(\"{word[1:]}\")")
        elif word in sp.__dict__:
            expr = expr.replace(word, "sp." + word)
        else:
            expr = expr.replace(word, f"sp.symbols(\"{word}\")")

    try:
        res = sp.pretty(eval(expr), use_unicode=True)
    except (SyntaxError, TypeError,
            ZeroDivisionError, ValueError) as err:
        await message.channel.send(err)
        return
    mes = f"""```{res}```"""
    await message.channel.send(mes)
