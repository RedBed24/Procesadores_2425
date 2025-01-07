from dataclasses import dataclass

from .secuencia import Secuencia


@dataclass
class Ligadura:
    secuencias: list[Secuencia]
