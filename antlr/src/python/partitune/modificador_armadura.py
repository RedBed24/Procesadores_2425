from enum import Enum


class ModificadorArmadura(Enum):
    SOSTENIDO = "#"
    BEMOL = "b"


def get_modificador_armadura_from_partitune(modificador: str) -> ModificadorArmadura:
    match modificador:
        case "#":
            return ModificadorArmadura.SOSTENIDO
        case "b":
            return ModificadorArmadura.BEMOL
        case _:
            raise ValueError(f"Modificador de armadura no válido: {modificador}")
