from pathlib import Path
from typing import List

import discord
import pydub

from metadata import get_metadata, get_sounds, get_raw_sounds
from player import get_player


def is_sound_command(sound_name: str) -> bool:
    """Checks whether an mp3 file with given name exists"""
    sounds = get_sounds()
    return sound_name + ".mp3" in sounds


def filter_sound_commands(*cmds) -> List[str]:
    """Filters commands that aren't valid soundcommands from lis"""
    return list(filter(is_sound_command, cmds))


def process_sound_commands(*cmds) -> List["SoundClip"]:
    """Turns list of sound commands to list of `SoundClip`s"""
    return [SoundClip(x) for x in cmds]


def normalize_audio_clips():
    """Normalizes all available audioclips"""
    in_path = get_metadata().paths.sounds
    out_path = get_metadata().paths.sounds_normalized
    out_path.mkdir(exist_ok=True)

    n_sounds = len(get_raw_sounds())
    for idx, sound_name in enumerate(get_raw_sounds()):
        percent_done = idx / n_sounds
        print(f"\x1b[1K\r[{'#' * int(10 * percent_done):.<10}] Normalizing: {sound_name}", end="")
        sound_path = Path(in_path, sound_name)
        sound = pydub.AudioSegment.from_file(sound_path)
        norm_sound = sound.apply_gain(-20 - sound.dBFS)
        norm_sound.export(Path(out_path, sound_name))
    print("\x1b[1K\rAudio normalization done.")


async def play_sound_commands(message: discord.Message, *cmds: List[str]):
    """Plays list of sound commands on associated `Player`"""
    cmds = filter_sound_commands(*cmds)
    cmds = process_sound_commands(*cmds)

    guild_id = message.guild.id
    player = get_player(guild_id)

    await player.connect_to_vc(message.author.voice.channel)
    await player.add_to_queue(*cmds)


class SoundClip:
    def __init__(self, cmd: str):
        self.path = Path(get_metadata().paths.sounds_normalized, cmd + ".mp3").resolve()

    def source(self):
        return discord.FFmpegOpusAudio(self.path)
