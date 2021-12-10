from typing import List

import yaml
import os
import pathlib
from dataclasses import dataclass


@dataclass()
class Metadata:
    @dataclass
    class Paths:
        sounds: pathlib.Path
        sounds_normalized: pathlib.Path
        logs: pathlib.Path

    paths: Paths


def root_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent


def metadata_path() -> pathlib.Path:
    return pathlib.Path(root_dir(), "metadata.yaml")


def read_metadata() -> dict:
    """Reads and returns raw metadata."""
    with open(metadata_path().resolve(), "r") as fd:
        return yaml.safe_load(fd)


def get_metadata() -> "Metadata":
    """Returns """
    meta = read_metadata()
    return Metadata(
        Metadata.Paths(
            pathlib.Path(root_dir(), meta["paths"]["sounds"]).resolve(),
            pathlib.Path(root_dir(), meta["paths"]["sounds_normalized"]).resolve(),
            pathlib.Path(root_dir(), meta["paths"]["logs"]).resolve(),
        )
    )


def get_sounds() -> List[str]:
    meta = get_metadata()
    return os.listdir(meta.paths.sounds_normalized)
