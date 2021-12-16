import inspect
import re
from io import BytesIO

import discord
import numpy as np
import sympy as sp

from metadata import get_sounds
from player import get_player

ALL_COMMANDS = dict()


def register_command(*names):
    """ Registers command to command dict. """

    def _register_command(func):
        for name in names:
            ALL_COMMANDS[name] = func
        return func

    return _register_command


@register_command("commands", "help")
async def commands(message: discord.Message):
    """Lists all commands."""
    mes = """Currently available commands:```"""
    for k in sorted(ALL_COMMANDS.keys()):
        mes += k + "\n"
    mes += """```Use `whatis [cmd]` to get additional information for specific command."""
    await message.channel.send(mes)


@register_command("whatis")
async def whatis(message: discord.Message, target: str):
    """Prints docstring for `[cmd]`."""
    if target in ALL_COMMANDS:
        func = ALL_COMMANDS[target]

        signature = target
        for k, v in inspect.signature(func).parameters.items():
            if k == "message":
                continue

            if v.default != v.empty:
                signature += fr" [{v.name} = {v.default}]"
            else:
                signature += fr" [{v.name}]"

        doc = func.__doc__

        await message.channel.send(f"`{signature}`\n\n{doc}")


@register_command("vcommands")
async def vcommands(message: discord.Message, ncols: int = 5):
    """Lists all available voice commands. Amount of columns can be specified by `<ncols>`."""
    sounds = np.array([x.split(".mp3")[0] for x in get_sounds()], dtype=object)
    sounds.sort()

    ncols = int(ncols)
    nrows = 1 + len(sounds) // ncols

    # Pad and reshape sound list
    sounds.resize((1, ncols * nrows))
    sounds[sounds == 0] = ""
    sounds = sounds.reshape((nrows, ncols))

    for idx in range(ncols - 1):
        max_len = max([len(x) for x in sounds.T[idx]]) + 3
        sounds.T[idx] = [x.ljust(max_len) for x in sounds.T[idx]]

    sounds = "\n".join(["".join(x) for x in sounds])
    await message.channel.send("```" + sounds + "```")


@register_command("leave", "skrid")
async def vc_leave(message: discord.Message):
    """Disconnects bot from voice channel."""
    guild_id = message.guild.id
    player = get_player(guild_id)

    await player.disconnect()


@register_command("test")
async def test(message: discord.Message):
    """Simply writes "Test" in channel."""
    await message.channel.send("Test")


@register_command("echo")
async def echo(message: discord.Message, *params):
    """Echoes the message specified by `[message]`."""
    if len(params) > 0:
        await message.channel.send(" ".join(params))


@register_command("hello")
async def hello(message: discord.Message):
    """Greets user."""
    await message.channel.send(f"Hello {message.author.name}!")


# @register_command("purge")
async def purge_channel(message: discord.Message):
    """Deletes all messages in channel."""
    await message.channel.purge()


@register_command("asciimath")
async def asciimath(message: discord.Message, *expr):
    """Evaluates `[expr]` using `Sympy`, and renders LaTeX math."""
    expr = " ".join(expr)
    expr = expr.replace("[", r"[")
    words = set(re.findall(r"[^\d\s()+*/\\\-,\[\]]+", expr))

    for word in words:
        if word in ["True", "False"]:
            continue
        elif word.startswith("'"):
            expr = re.sub(fr"(?<=\b){word}(?=\b)", f"sp.symbols(\"{word[1:]}\")", expr)
        elif word in sp.__dict__:
            expr = re.sub(fr"(?<=\b){word}(?=\b)", "sp." + word, expr)
        else:
            expr = re.sub(fr"(?<=\b){word}(?=\b)", f"sp.symbols(\"{word}\")", expr)

    try:
        preamble = "\\documentclass[margin=5mm]{standalone}\n" \
                   "\\usepackage{amsmath,amsfonts}\n" \
                   "\\begin{document}" \
                   "\\Huge"

        image_obj = BytesIO()
        sp.preview(f"${sp.latex(eval(expr))}$", output="png", viewer="BytesIO", outputbuffer=image_obj,
                   preamble=preamble)
        image_obj.seek(0)

        file = discord.File(image_obj, filename="result.png")
        await message.channel.send(file=file)
    except (SyntaxError, TypeError,
            ZeroDivisionError, ValueError) as err:
        await message.channel.send(err)
        return


@register_command("asd")
async def asd(message):
    await message.channel.send("asd")
