"""Módulo para la representación del compás de una partitura."""
from enum import Enum


class Compas(Enum):
    """Enum para representar el compás de una partitura.
    
    Valores
    -------
    
    - DOSPORCUATRO: Compás de 2/4.
    - TRESPORCUATRO: Compás de 3/4.
    - CUATROPORCUATRO: Compás de 4/4.
    - SEISPOROCHO: Compás de 6/8.
    """
    DOSPORCUATRO = "2/4"
    TRESPORCUATRO = "3/4"
    CUATROPORCUATRO = "4/4"
    SEISPOROCHO = "6/8"


def get_compas_from_partitune(compas: str) -> Compas:
    """Obtiene el compás de una partitura a partir de su representación en Partitune.
    
    :param compas: El compás de la partitura en Partitune. Uno entre ["2/4", "3/4", "4/4", "6/8"].

    :returns: El compás de la partitura.

    :raises ValueError: Si el compás no es válido.
    """
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
