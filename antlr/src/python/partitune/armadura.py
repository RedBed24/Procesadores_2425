from dataclasses import dataclass

from .nota import NotaBase
from .modificador_armadura import ModificadorArmadura


@dataclass
class Armadura:
    cantidad_modificadores: int # TODO: Assign a value to this field!
    tipo_modificacion: ModificadorArmadura

    def __init__(self, tipo_modificacion: ModificadorArmadura, notas: list[NotaBase]):
        self.tipo_modificacion = tipo_modificacion
        if validate_armadura(tipo_modificacion, notas):
            self.cantidad_modificadores = len(notas)
        else:
            self.cantidad_modificadores = 0


def validate_armadura(
    tipo_modificacion: ModificadorArmadura, notas_a_validar: list[NotaBase]
) -> bool:
    notas_posibles: list[NotaBase]
    match tipo_modificacion:
        case ModificadorArmadura.BEMOL:
            notas_posibles = [
                NotaBase.SI,
                NotaBase.MI,
                NotaBase.LA,
                NotaBase.RE,
                NotaBase.SOL,
                NotaBase.DO,
                NotaBase.FA,
            ]
        case ModificadorArmadura.SOSTENIDO:
            notas_posibles = [
                NotaBase.FA,
                NotaBase.DO,
                NotaBase.SOL,
                NotaBase.RE,
                NotaBase.LA,
                NotaBase.MI,
                NotaBase.SI,
            ]

    if not notas_a_validar:
        return False

    cuenta: list[int] = [0] * len(notas_posibles)

    for nota in notas_a_validar:
        cuenta[notas_posibles.index(nota)] += 1

    for i, cantidad in enumerate(cuenta):
        if cantidad == 0:
            break

    return all(cantidad == 0 for cantidad in cuenta[i + 1 :])
