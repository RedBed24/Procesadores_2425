"""Módulo para la representación de la clave de una partitura."""
from enum import Enum


class Clave(Enum):
    """Enum para representar la clave de una partitura.
    
    Valores
    -------

    - SOL: Clave de sol.
    - FA: Clave de fa.
    - DO: Clave de do.
    """
    SOL = "SOL"
    FA = "FA"
    DO = "DO"


def get_clave_from_partitune(clave: str) -> Clave:
    """Obtiene la clave de una partitura a partir de su representación en Partitune.
    
    :param clave: La clave de la partitura en Partitune. Una entre ["SOL", "FA", "DO"]. Sin importar mayúsculas o minúsculas.
    
    :returns: La clave de la partitura.

    :raises ValueError: Si la clave no es válida.
    """
    match clave.upper():
        case "SOL":
            return Clave.SOL
        case "FA":
            return Clave.FA
        case "DO":
            return Clave.DO
        case _:
            raise ValueError(clave)
