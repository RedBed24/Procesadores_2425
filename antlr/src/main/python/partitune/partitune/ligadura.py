from .secuencia import Secuencia


# Ligadura de secuencias
class Ligadura:
    def __init__(self, secuencias: list[Secuencia]):
        self.secuencias = validate_ligadura(secuencias)

def validate_ligadura(secuencias: list[Secuencia]) -> list[Secuencia]:
    if any(any(not nota for nota in secuencia) for secuencia in secuencias):
        raise ValueError("No debe haber silencios en las secuencias de la ligadura.")

    if len(secuencias) == 1 and all(len(secuencia) == 1 for secuencia in secuencias):
        raise AttributeError("Las ligaduras deben tener al menos 2 notas")

    return secuencias

