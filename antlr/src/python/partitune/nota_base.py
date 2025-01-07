from enum import Enum


class NotaBase(Enum):
    DO = "DO"
    RE = "RE"
    MI = "MI"
    FA = "FA"
    SOL = "SOL"
    LA = "LA"
    SI = "SI"


def get_nota_base_from_partitune(nota_base: str) -> NotaBase:
    match nota_base.upper():
        case "DO":
            return NotaBase.DO
        case "RE":
            return NotaBase.RE
        case "MI":
            return NotaBase.MI
        case "FA":
            return NotaBase.FA
        case "SOL":
            return NotaBase.SOL
        case "LA":
            return NotaBase.LA
        case "SI":
            return NotaBase.SI
        case _:
            raise ValueError(f"Invalid note: {nota_base}")
