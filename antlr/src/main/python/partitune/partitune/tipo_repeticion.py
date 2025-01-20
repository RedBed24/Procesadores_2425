"""Modulo que contiene la enumeracion de los tipos de repeticion."""
from enum import Enum

# Tipo de repeticiones posibles en partituras
class TipoRepeticion(Enum):
    """Enum para representar los tipos de repeticion en una partitura.

    Valores
    -------

    - CON_INICIO: Repetición con inicio.
    - SIN_INICIO: Repetición sin inicio.
    """
    CON_INICIO = 0
    SIN_INICIO = 1
