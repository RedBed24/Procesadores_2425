"""Módulo para la representación de la duración de una nota."""
from enum import Enum


class Duracion(Enum):
    """Enum para representar la duración de una nota.
    
    Valores
    -------
    
    - SEMIFUSA: Duración de una semifusa.
    - FUSA: Duración de una fusa.
    - SEMICORCHEA: Duración de una semicorchea.
    - CORCHEA: Duración de una corchea.
    - NEGRA: Duración de una negra.
    - BLANCA: Duración de una blanca.
    - REDONDA: Duración de una redonda.
    """
    SEMIFUSA = "SF"
    FUSA = "F"
    SEMICORCHEA = "SC"
    CORCHEA = "C"
    NEGRA = "N"
    BLANCA = "BL"
    REDONDA = "R"


def get_duracion_from_partitune(duracion: str) -> Duracion:
    """Obtiene la duración de una nota a partir de su representación en Partitune.
    
    :param duracion: La duración de la nota en Partitune. Una entre ["SF", "F", "SC", "C", "N", "BL", "R"]. Sin importar mayúsculas o minúsculas.

    :returns: La duración de la nota.

    :raises ValueError: Si la duración no es válida.
    """
    match duracion.upper():
        case "SF":
            return Duracion.SEMIFUSA
        case "F":
            return Duracion.FUSA
        case "SC":
            return Duracion.SEMICORCHEA
        case "C":
            return Duracion.CORCHEA
        case "N":
            return Duracion.NEGRA
        case "BL":
            return Duracion.BLANCA
        case "R":
            return Duracion.REDONDA
        case _:
            raise ValueError(f"Invalid duration: {duracion}")
