"""Módulo que define la clase Armadura y su reconocedor."""
from dataclasses import dataclass

from .nota import NotaBase
from .modificador_armadura import ModificadorArmadura


@dataclass
class Armadura:
    """Clase que representa una armadura en una partitura."""
    cantidad_modificadores: int  # entre 1 y 7
    tipo_modificacion: ModificadorArmadura

    def __init__(self, tipo_modificacion: ModificadorArmadura, notas: list[NotaBase]):
        """Constructor de la clase Armadura.
        
        :param tipo_modificacion: Tipo de modificación de la armadura.
        :param notas: Notas que se ven afectadas por la armadura."""
        self.tipo_modificacion = tipo_modificacion
        self.cantidad_modificadores = validate_armadura(tipo_modificacion, notas)


# Función que valida si las notas son correctas para una armadura dada un tipo de modificación
def validate_armadura(
    tipo_modificacion: ModificadorArmadura, notas_a_validar: list[NotaBase]
) -> int:
    """Valida que la armadura sea válida. Esto es, comprueba que dado el modificador, aparezcan las notas correctas.
    Se considera correcta si en la lista de notas aparecen todas las notas al menos 1 vez hasta la nota i de las notas
    posibles, y no aparecen las notas después de la nota i.
    
    :param tipo_modificacion: Tipo de modificación de la armadura.
    :param notas_a_validar: Notas que se ven afectadas por la armadura. Pueden estar dupilcadas. No se requiere orden.
    
    :return: Cantidad de modificadores de la armadura. Valor entre 1 y 7.
    """
    notas_posibles: list[NotaBase]
    match tipo_modificacion:
        case ModificadorArmadura.BEMOL:
            notas_posibles = [
                NotaBase.SI,
                NotaBase.MI,
                NotaBase.LA,
                NotaBase.RE, # si ha aparecido esta, deben haber aparecido todas las anteriores
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
            
    # Si no se especifican notas, se lanza un error
    if not notas_a_validar:
        raise ValueError("No se han especificado notas para la armadura.")

    cuenta: list[int] = [0] * len(notas_posibles)

    # contamos cuántas veces aparece cada nota
    for nota in notas_a_validar:
        cuenta[notas_posibles.index(nota)] += 1

    if all(cantidad != 0 for cantidad in cuenta):
        # todas las notas están presentes
        return 7

    # vemos hasta qué nota (supestamente) están presentes
    for i, cantidad in enumerate(cuenta):
        if cantidad == 0:
            break

    if any(cantidad != 0 for cantidad in cuenta[i + 1 :]):
        # no hay nota i pero sí notas después de i
        raise ValueError("Las notas de la armadura no es válida.")

    return i
