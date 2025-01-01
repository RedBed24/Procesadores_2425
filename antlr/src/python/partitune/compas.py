from enum import Enum


class Compas(Enum):
    DOSPORCUATRO = "2/4"
    TRESPORCUATRO = "3/4"
    CUATROPORCUATRO = "4/4"
    SEISPOROCHO = "6/8"


def get_compas_from_partitune(compas: str) -> Compas:
    match compas.lower():
        case "2/4":
            return Compas.DOSPORCUATRO
        case "3/4":
            return Compas.TRESPORCUATRO
        case "4/4":
            return Compas.CUATROPORCUATRO
        case "6/8":
            return Compas.SEISPOROCHO
        case _:
            raise ValueError(f"Invalid compas: {compas}")
