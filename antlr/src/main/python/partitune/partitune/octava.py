from enum import Enum


class Octava(Enum):
    GRAVE = 0
    NORMAL = 1
    AGUDO = 2


def get_octava_from_partitune(octava: str) -> Octava:
    match octava:
        case "'":
            return Octava.AGUDO
        case "":
            return Octava.NORMAL
        case "_":
            return Octava.GRAVE
        case _:
            raise ValueError(f"Invalid octave: {octava}")
