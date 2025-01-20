from dataclasses import dataclass

from .secuencia import Secuencia

# Ligadura de secuencias
@dataclass
class Ligadura:
    secuencias: list[Secuencia]
