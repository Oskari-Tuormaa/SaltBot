import pathlib
from dataclasses import dataclass
from typing import List

import yaml


@dataclass()
class Metadata:
    @dataclass
    class Paths:
        sounds: pathlib.Path
        sounds_normalized: pathlib.Path
        logs: pathlib.Path

    paths: Paths


def root_dir() -> pathlib.Path:
    """Returns root directory"""
    return pathlib.Path(__file__).parent.parent


def metadata_path() -> pathlib.Path:
    """Returns path to metadata.yaml"""
    return pathlib.Path(root_dir(), "metadata.yaml")


def read_metadata() -> dict:
    """Reads and returns raw metadata."""
    with open(metadata_path().resolve(), "r") as fd:
        return yaml.safe_load(fd)


def get_metadata() -> "Metadata":
    """Returns populated `Metadata` object"""
    meta = read_metadata()
    return Metadata(
        Metadata.Paths(
            pathlib.Path(root_dir(), meta["paths"]["sounds"]).resolve(),
            pathlib.Path(root_dir(), meta["paths"]["sounds_normalized"]).resolve(),
            pathlib.Path(root_dir(), meta["paths"]["logs"]).resolve(),
        )
    )


def get_raw_sounds() -> List[str]:
    """Returns list of all unnormalized sound files"""
    meta = get_metadata()
    return [x.name for x in meta.paths.sounds.iterdir() if x.is_file()]


def get_sounds() -> List[str]:
    """Returns list of all sound commands"""
    meta = get_metadata()
    return [x.name for x in meta.paths.sounds_normalized.iterdir() if x.is_file()]
