from typing import List

import yaml
import os
from dataclasses import dataclass


@dataclass()
class Metadata:
    @dataclass
    class Paths:
        sounds: str
        sounds_normalized: str

    paths: Paths


def read_metadata() -> dict:
    """Reads and returns raw metadata."""
    with open("../metadata.yaml", "r") as fd:
        return yaml.safe_load(fd)


def get_metadata() -> "Metadata":
    """Returns """
    meta = read_metadata()
    return Metadata(
        Metadata.Paths(
            os.path.abspath("../" + meta["paths"]["sounds"]),
            os.path.abspath("../" + meta["paths"]["sounds_normalized"])
        )
    )


def get_sounds() -> List[str]:
    meta = get_metadata()
    return os.listdir(meta.paths.sounds_normalized)
