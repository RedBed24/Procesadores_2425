from src.python.generacion import _generar_lineas_divisorias as _gld
from src.python.partitune.compas import Compas


dos = Compas.DOSPORCUATRO
tres = Compas.TRESPORCUATRO
cuatro = Compas.CUATROPORCUATRO
seis = Compas.SEISPOROCHO

texto_notas = '''A1/4 A1 A1/4 A1/2 A2'''
assert _gld(texto_notas,  dos) == '''A1/4 A1 A1/4 A1/2 | A2 | \n''' # notas simples
assert _gld(texto_notas,  tres) == '''A1/4 A1 A1/4 A1/2 z1 | A2 \n''' # necesita silencios para rellenar compases
assert _gld(texto_notas,  cuatro) == '''A1/4 A1 A1/4 A1/2 A2 | \n'''

corcheas_2pulsos = '''A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4'''
assert _gld(corcheas_2pulsos,  dos) == '''A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 | \n''' # justo dos
assert _gld(corcheas_2pulsos,  tres) == '''A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 \n''' # queda sin cerrar porque despues pueden venir mas notas
assert _gld(corcheas_2pulsos,  cuatro) == '''A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 A1/4 \n''' # sin cerrar compas

rellenar_silencios = "A2 A1/2 A1 A1/4 A1/4 A2"
assert _gld(rellenar_silencios,  tres) == "A2 A1/2 z1/2 | A1 A1/4 A1/4 z3/2 | A2 \n"

valor_mayor = 'A1 A3 A4 A6 A1'
assert _gld(valor_mayor,  dos) == 'A1 A3 | A4 | A6 | A1 \n' # notas mayores apaño

repeticion= '|: A1 A1 A1 A1/2 :| A2'
assert _gld(repeticion,  dos) == '|: A1 A1 | A1 A1/2 z1/2 :| A2 | \n' # repeticion añade silencios
assert not _gld(repeticion,  tres) == '|: A1 A1 | A1 A1/2 z1/2 :| A2 | \n' # repeticion añade silencios

fragmento_3 = "A1/4 A1 A1/4 A1/2 A2\nK:C\nM:3/4\nA1/4 A1 A1/4 A1/2 A2"
assert _gld(fragmento_3,  dos) == "A1/4 A1 A1/4 A1/2 | A2 | \nK:C\nM:3/4\nA1/4 A1 A1/4 A1/2 z1 | A2 \n"

fragmento_2 = "A1/4 A1 A1/4 A1/2 A2\nK:C\nM:2/4\nA1/4 A1 A1/4 A1/2 A2"
assert _gld(fragmento_2,  tres) == "A1/4 A1 A1/4 A1/2 z1 | A2 \nK:C\nM:2/4\nA1/4 A1 A1/4 A1/2 | A2 | \n"

silencios = 'a1/16 ,a2 A1/8 A2'
assert _gld(silencios,  dos) == 'a1/16 z1 z15/16 | ,a2 | A1/8 z1 z7/8 | A2 | \n'

