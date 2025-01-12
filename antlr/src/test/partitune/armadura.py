from src.python.partitune.armadura import ModificadorArmadura as MA, validate_armadura as va
from src.python.partitune.nota_base import NotaBase as NB

B = MA.BEMOL; S = MA.SOSTENIDO
DO = NB.DO; RE = NB.RE; MI = NB.MI; FA = NB.FA; SOL = NB.SOL; LA = NB.LA; SI = NB.SI


def raises(f, *args):
    try:
        f(*args)
        return False
    except ValueError:
        return True

assert raises(va, B, []),                                 "No se puede tener armadura sin notas"
assert raises(va, S, []),                                 "No se puede tener armadura sin notas"
assert    1 == va(B, [SI]),                               "Una armadura de bemol puede tener una nota SI"
assert    1 == va(B, [SI]*2),                             "Una armadura de bemol puede tener dos notas SI, se entiende que es la misma nota"
assert    2 == va(B, [SI, MI]),                           "Una armadura de bemol puede tener dos notas SI y MI"
assert    2 == va(B, [MI, SI]),                           "Una armadura de bemol puede tener dos notas MI y SI, sin importar el orden"
assert raises(va, B, [MI]),                               "Si una armadura de bemol tiene una nota MI, debe tener una SI"
assert    3 == va(B, [SI, MI, LA]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA"
assert    3 == va(B, [MI, SI, LA]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA, sin importar el orden"
assert    3 == va(B, [LA, SI, MI]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA, sin importar el orden"
assert raises(va, B, [SI, LA]),                           "Si una armadura de bemol tiene una nota LA, debe tener una MI"
assert raises(va, B, [MI, LA]),                           "Si una armadura de bemol tiene una nota LA, debe tener una SI"
assert raises(va, B, [LA]),                               "Si una armadura de bemol tiene una nota LA, debe tener SI y MI"
assert    4 == va(B, [SI, MI, LA, RE])
assert    5 == va(B, [SI, MI, LA, RE, SOL])
assert    6 == va(B, [SI, MI, LA, RE, SOL, DO])
assert    7 == va(B, [SI, MI, LA, RE, SOL, DO, FA])
assert    7 == va(B, [SI, MI, LA, RE, SOL, DO, FA, FA])
assert    1 == va(S, [FA])
assert    2 == va(S, [FA, DO])
assert    3 == va(S, [FA, DO, SOL])
assert    4 == va(S, [FA, DO, SOL, RE])
assert    5 == va(S, [FA, DO, SOL, RE, LA])
assert    6 == va(S, [FA, DO, SOL, RE, LA, MI])
assert    7 == va(S, [FA, DO, SOL, RE, LA, MI, SI])
