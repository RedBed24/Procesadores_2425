from enum import Enum


class Clave(Enum):
    SOL = "SOL"
    FA = "FA"
    DO = "DO"

# Claves posibles en partituras
def get_clave_from_partitune(clave: str) -> Clave:
    match clave.upper():
        case "SOL":
            return Clave.SOL
        case "FA":
            return Clave.FA
        case "DO":
            return Clave.DO
        case _:
            raise ValueError(clave)
