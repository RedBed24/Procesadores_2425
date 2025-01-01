from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel


class ModificadorArmadura(Enum):
    SOSTENIDO = "'"
    BEMOL = "b"


def get_modificador_armadura_from_partitune(modificador: str) -> ModificadorArmadura:
    match modificador:
        case "'":
            return ModificadorArmadura.SOSTENIDO
        case "b":
            return ModificadorArmadura.BEMOL
        case _:
            raise ValueError(f"Modificador de armadura no válido: {modificador}")


@dataclass
class Armadura(BaseModel):
    cantidad_modificadores: int
    tipo_modificacion: ModificadorArmadura

    def validar(self):
        if self.cantidad_modificadores < 0:
            raise ValueError("La cantidad de modificadores no puede ser negativa.")
        if self.cantidad_modificadores > 7:
            raise ValueError("La cantidad de modificadores no puede ser mayor a 7.")
