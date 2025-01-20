"""Módulo para la representación de las ligaduras de una partitura."""
from .secuencia import Secuencia


class Ligadura:
    """Representa una ligadura de una partitura."""
    def __init__(self, secuencias: list[Secuencia]):
        """Constructor de la ligadura.
        
        :param secuencias: Las secuencias de notas que conforman la ligadura.
        
        :raises ValueError: Si alguna secuencia de la ligadura tiene silencios.
        :raises AttributeError: Si la ligadura tiene menos de 2 notas.
        """
        self.secuencias = validate_ligadura(secuencias)

def validate_ligadura(secuencias: list[Secuencia]) -> list[Secuencia]:
    """Valida las secuencias de la ligadura.
    
    :param secuencias: Las secuencias de notas que conforman la ligadura.
    
    :raises ValueError: Si alguna secuencia de la ligadura tiene silencios.
    :raises AttributeError: Si la liga tiene menos de 2 notas.
    
    :return: Las secuencias de la ligadura."""
    if any(any(not nota for nota in secuencia) for secuencia in secuencias):
        # si alguna de las secuencias tiene alguna no nota (silencio)
        raise ValueError("No debe haber silencios en las secuencias de la ligadura.")

    if len(secuencias) == 1 and all(len(secuencia) == 1 for secuencia in secuencias):
        # si sólo hay una secuencia y todas las secuencias (la única que hay) tienen una sola nota
        raise AttributeError("Las ligaduras deben tener al menos 2 notas")

    return secuencias

