from enum import Enum


class Duracion(Enum):
    SEMIFUSA = "SF"
    FUSA = "F"
    SEMICORCHEA = "SC"
    CORCHEA = "C"
    NEGRA = "N"
    BLANCA = "BL"
    REDONDA = "R"


def get_duracion_from_partitune(duracion: str) -> Duracion:
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
