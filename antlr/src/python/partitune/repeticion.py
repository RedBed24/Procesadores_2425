from dataclasses import dataclass

from .secuencia import Secuencia
from .tipo_repeticion import TipoRepeticion


@dataclass
class Repeticion:
    tipo_repeticion: TipoRepeticion
    secuencias: list[Secuencia]
