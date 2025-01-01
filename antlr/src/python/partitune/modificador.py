from enum import Enum


class Modificador(Enum):
    SOSTENIDO = "#"
    BEMOL = "b"
    BECUADRO = "%"


def get_modificador_from_partitune(modificador: str) -> Modificador:
    match modificador:
        case "#":
            return Modificador.SOSTENIDO
        case "b" | "B":
            return Modificador.BEMOL
        case "%":
            return Modificador.BECUADRO
        case _:
            raise ValueError(f"Invalid modificador: {modificador}")
