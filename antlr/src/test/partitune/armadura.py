from src.python.partitune.armadura import ModificadorArmadura as MA, validate_armadura as va
from src.python.partitune.nota_base import NotaBase as NB

B = MA.BEMOL; S = MA.SOSTENIDO
DO = NB.DO; RE = NB.RE; MI = NB.MI; FA = NB.FA; SOL = NB.SOL; LA = NB.LA; SI = NB.SI

assert not va(B, []),                                 "No se puede tener armadura sin notas"
assert not va(S, [])
assert     va(B, [SI]),                               "Una armadura de bemol puede tener una nota SI"
assert     va(B, [SI]*2),                             "Una armadura de bemol puede tener dos notas SI, se entiende que es la misma nota"
assert     va(B, [SI, MI]),                           "Una armadura de bemol puede tener dos notas SI y MI"
assert     va(B, [MI, SI]),                           "Una armadura de bemol puede tener dos notas MI y SI, sin importar el orden"
assert not va(B, [MI]),                               "Si una armadura de bemol tiene una nota MI, debe tener una SI"
assert     va(B, [SI, MI, LA]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA"
assert     va(B, [MI, SI, LA]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA, sin importar el orden"
assert     va(B, [LA, SI, MI]),                       "Una armadura de bemol puede tener tres notas SI, MI y LA, sin importar el orden"
assert not va(B, [SI, LA]),                           "Si una armadura de bemol tiene una nota LA, debe tener una MI"
assert not va(B, [MI, LA]),                           "Si una armadura de bemol tiene una nota LA, debe tener una SI"
assert not va(B, [LA]),                               "Si una armadura de bemol tiene una nota LA, debe tener SI y MI"
assert     va(B, [SI, MI, LA, RE])
assert     va(B, [SI, MI, LA, RE, SOL])
assert     va(B, [SI, MI, LA, RE, SOL, DO])
assert     va(B, [SI, MI, LA, RE, SOL, DO, FA])
assert     va(B, [SI, MI, LA, RE, SOL, DO, FA, FA])
assert     va(S, [FA])
assert     va(S, [FA, DO])
assert     va(S, [FA, DO, SOL])
assert     va(S, [FA, DO, SOL, RE])
assert     va(S, [FA, DO, SOL, RE, LA])
assert     va(S, [FA, DO, SOL, RE, LA, MI])
assert     va(S, [FA, DO, SOL, RE, LA, MI, SI])
