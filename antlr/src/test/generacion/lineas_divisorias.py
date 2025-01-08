from src.python.generacion import _generar_lineas_divisorias as _gld
from src.python.partitune.compas import Compas

texto = '''
A1/4 A1 A1/4 A1/2 A2
'''

dos = Compas.DOSPORCUATRO
tres = Compas.TRESPORCUATRO
cuatro = Compas.CUATROPORCUATRO
seis = Compas.SEISPOROCHO
print(_gld(texto,  dos))

assert _gld(texto,  dos) == '''A1/4 A1 A1/4 A1/2 | A2'''

