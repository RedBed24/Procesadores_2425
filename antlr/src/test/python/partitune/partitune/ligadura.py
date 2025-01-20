from partitune.partitune.ligadura import validate_ligadura as vl
from partitune.partitune.secuencia import Secuencia as S

a = AttributeError
v = ValueError

def raises(e, f, *args):
    try:
        f(*args)
        return False
    except e:
        return True
    except:
        return False

assert raises(a, vl, [S(0, [True])]),               "No se puede tener ligadura con sólo una nota"
assert           vl ([S(0, [True]), S(0, [True])]), "Se puede tener ligadura con dos notas en distinta secuencia"
assert           vl ([S(0, [True, True])]),         "Se puede tener ligadura con dos notas en misma secuencia"
assert raises(v, vl, [S(0, [True]), S(0, [None])]), "No se puede tener ligadura con silencios"