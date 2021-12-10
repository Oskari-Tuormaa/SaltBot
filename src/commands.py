import re

import discord
import numpy as np
import sympy as sp

from metadata import get_sounds
from player import get_player

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

    Prints docstring for `[cmd]`."""
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
    mes = """Currently available commands:```"""
    for k in ALL_COMMANDS.keys():
        mes += k + "\n"
    mes += "```"
    await message.channel.send(mes)


@register_command("vcommands")
async def vcommands(message: discord.Message, ncols: int = 5):
    """`vcommands [ncols]`

    Lists all available voice commands. Amount of columns can be specified by `<ncols>`."""
    sounds = np.array([x.split(".mp3")[0] for x in get_sounds()], dtype=object)
    sounds.sort()

    ncols = int(ncols)

    # Pad sound list
    to_pad = ncols - (len(sounds) % ncols)
    if to_pad != 1:
        sounds = np.append(sounds, [""]*to_pad)

    sounds = sounds.reshape((-1, ncols))

    for idx in range(ncols-1):
        max_len = max([len(x) for x in sounds.T[idx]]) + 3
        sounds.T[idx] = [x.ljust(max_len) for x in sounds.T[idx]]

    sounds = "\n".join(["".join(x) for x in sounds])
    await message.channel.send("```"+sounds+"```")


@register_command("leave")
async def vc_leave(message: discord.Message):
    """`leave`

    Disconnects bot from voice channel."""
    guild_id = message.guild.id
    player = get_player(guild_id)

    await player.disconnect()


@register_command("test")
async def test(message: discord.Message):
    """`test`

    Simply writes "Test" in channel."""
    await message.channel.send("Test")


@register_command("echo")
async def echo(message: discord.Message, *params):
    """`echo [message]`

    Echoes the message specified by `[message]`."""
    if len(params) > 0:
        await message.channel.send(" ".join(params))


@register_command("hello")
async def hello(message: discord.Message):
    """`hello`

    Greets user."""
    await message.channel.send(f"Hello {message.author.name}!")


# @register_command("purge")
async def purge_channel(message: discord.Message):
    """`purge`

    Deletes all messages in channel."""
    await message.channel.purge()


@register_command("asciimath")
async def asciimath(message: discord.Message, *expr):
    """`asciimath [expr]`

    Evaluates `[expr]` using `Sympy`."""
    expr = " ".join(expr)
    words = set(re.findall(r"[^\d\s()+*/\-,]+", expr))

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
