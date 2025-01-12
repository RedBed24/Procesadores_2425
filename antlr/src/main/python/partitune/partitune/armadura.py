from dataclasses import dataclass

from .nota import NotaBase
from .modificador_armadura import ModificadorArmadura


@dataclass
class Armadura:
    cantidad_modificadores: int  # entre 1 y 7
    tipo_modificacion: ModificadorArmadura

    def __init__(self, tipo_modificacion: ModificadorArmadura, notas: list[NotaBase]):
        self.tipo_modificacion = tipo_modificacion
        self.cantidad_modificadores = validate_armadura(tipo_modificacion, notas)


def validate_armadura(
    tipo_modificacion: ModificadorArmadura, notas_a_validar: list[NotaBase]
) -> int:
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
        raise ValueError("No se han especificado notas para la armadura.")

    cuenta: list[int] = [0] * len(notas_posibles)

    for nota in notas_a_validar:
        cuenta[notas_posibles.index(nota)] += 1

    if all(cantidad != 0 for cantidad in cuenta):
        # todas las notas están presentes
        return 7

    for i, cantidad in enumerate(cuenta):
        if cantidad == 0:
            break

    if any(cantidad != 0 for cantidad in cuenta[i + 1 :]):
        # no hay nota i pero sí notas después de i
        raise ValueError("Las notas de la armadura no es válida.")

    return i
