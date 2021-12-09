import discord
import os
from commands import ALL_COMMANDS
from player import get_player
from typing import List
from metadata import get_metadata, get_sounds


def is_sound_command(sound_name: str) -> bool:
    sounds = get_sounds()
    return sound_name + ".mp3" in sounds


def filter_sound_commands(*cmds) -> List[str]:
    return list(filter(is_sound_command, cmds))


def process_sound_commands(*cmds) -> List["SoundClip"]:
    return [SoundClip(x) for x in cmds]


async def play_sound_commands(message: discord.Message, *cmds: List[str]):
    cmds = filter_sound_commands(*cmds)
    cmds = process_sound_commands(*cmds)

    guild_id = message.guild.id
    player = get_player(guild_id)

    await player.connect_to_vc(message.author.voice.channel)
    await player.add_to_queue(*cmds)


class SoundClip:
    def __init__(self, cmd: str):
        self.path = os.path.abspath(
            os.path.join(
                get_metadata().paths.sounds_normalized,
                cmd + ".mp3"
            )
        )

    def source(self):
        return discord.FFmpegOpusAudio(self.path)
