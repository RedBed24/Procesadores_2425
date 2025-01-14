from fractions import Fraction
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from .analysis.Scanner import Scanner
from .analysis.Parser import Parser
from .visitor import Visitor
from .partitune.obra import Obra
from .partitune.secuencia import Secuencia
from .partitune.repeticion import Repeticion
from .partitune.ligadura import Ligadura
from .partitune.nota import Nota
from .partitune.duracion import Duracion
from .partitune.compas import Compas
from .partitune.clave import Clave
from .partitune.armadura import Armadura
from .partitune.modificador import Modificador
from .partitune.fragmento import Fragmento
from .partitune.modificador_armadura import ModificadorArmadura
import re


def _duracion_to_abc(nota: Nota | None, duracion: Duracion) -> str:
    """
    Convierte un objeto Duracion en su representación de notación ABC.
    Se utiliza un mapeo para transformar duraciones musicales a su formato en ABC.
    """
    if nota and nota.puntillo:
        duracion_map = {
            Duracion.SEMIFUSA: "3/32",
            Duracion.FUSA: "3/16",
            Duracion.SEMICORCHEA: "3/8",
            Duracion.CORCHEA: "3/4",
            Duracion.NEGRA: "3/2",
            Duracion.BLANCA: "3",
            Duracion.REDONDA: "6",
        }
    else:
        duracion_map = {
            Duracion.SEMIFUSA: "1/16",
            Duracion.FUSA: "1/8",
            Duracion.SEMICORCHEA: "1/4",
            Duracion.CORCHEA: "1/2",
            Duracion.NEGRA: "1",
            Duracion.BLANCA: "2",
            Duracion.REDONDA: "4",
        }

    # Se devuelve la cadena correspondiente a la duración dada.
    return duracion_map.get(duracion, "")


def _procesar_nota(nota: Nota) -> str:
    """
    Convierte una Nota en su representación ABC, considerando modificadores,
    octava y puntillo.
    """
    # Mapeo de notas base del formato partitune a notación ABC estándar.
    nota_base_map = {
        "DO": "C", "RE": "D", "MI": "E", "FA": "F",
        "SOL": "G", "LA": "A", "SI": "B"
    }
    # Se obtiene la base de la nota correspondiente.
    base = nota_base_map.get(nota.nota_base.name, "C")

    # Mapeo de modificadores (sostenido, bemol, becuadro) a símbolos ABC.
    mod_map = {
        Modificador.SOSTENIDO: "^",
        Modificador.BEMOL: "_",
        Modificador.BECUADRO: "="
    }
    # Se obtiene el símbolo del modificador si existe.
    mod = mod_map.get(nota.modificador, "")

    # Ajuste de octava: para agudo se usa minúscula, para grave se añade coma.
    if nota.octava.name == "AGUDO":
        base = base.lower()
    elif nota.octava.name == "GRAVE":
        base += ","

    # Se devuelve la concatenación del modificador con la base ajustada.
    return mod + base


def _procesar_secuencia(secuencia: Secuencia) -> str:
    """
    Convierte una Secuencia en notación ABC, procesando cada nota o silencio.
    Itera sobre las notas de la secuencia y las traduce a formato ABC.
    """
    notas_abc = []
    # Procesar cada nota dentro de la secuencia.
    for nota in secuencia.lista_notas:
        if nota is None:
            # Si la nota es None, se trata de un silencio (pausa).
            notas_abc.append(f"z{_duracion_to_abc(nota, secuencia.duracion)}")
        else:
            # Si es una nota, se procesa con su duración.
            notas_abc.append(f"{_procesar_nota(nota)}{_duracion_to_abc(nota, secuencia.duracion)}")
    # Se unen todas las notas procesadas en una sola cadena separada por espacios.
    return " ".join(notas_abc)


def _procesar_repeticion(repeticion: Repeticion) -> str:
    """
    Convierte una Repetición en notación ABC, incluyendo marcadores de inicio y fin.
    Procesa todas las secuencias dentro de la repetición.
    """
    # Procesamos cada secuencia dentro de la repetición y las unimos con espacios.
    secuencias_abc = " ".join(_procesar_secuencia(s) for s in repeticion.secuencias)

    # Según el tipo de repetición, se agregan los marcadores de repetición ABC.
    if repeticion.tipo_repeticion.name == "CON_INICIO":
        return f"|: {secuencias_abc} :|"
    else:
        return f"{secuencias_abc} :|"


def _procesar_ligadura(ligadura: Ligadura) -> str:
    """
    Convierte una Ligadura en notación ABC, envolviendo cada secuencia entre paréntesis.
    """
    secuencias_abc = []
    # Iterar por cada secuencia en la ligadura.
    for secuencia in ligadura.secuencias:
        # Procesar cada nota en la secuencia.
        notas_abc = " ".join(
            # Si la nota es válida, se procesa normalmente.
            f"{_procesar_nota(nota)}{_duracion_to_abc(nota, secuencia.duracion)}" if nota
            # Si es silencio, se marca con 'z'.
            else f"z{_duracion_to_abc(nota, secuencia.duracion)}"
            for nota in secuencia.lista_notas
        )
        # Se envuelve la secuencia procesada entre paréntesis.
        secuencias_abc.append(f"({notas_abc})")
    # Se unen todas las secuencias ligadas con espacios y se devuelve.
    return " ".join(secuencias_abc)


def _parse_compas(compas: Compas) -> str:
    """
    Convierte un objeto Compas en su representación de cadena para ABC.
    """
    # Asume que el compás ya tiene un atributo 'value' representando su notación.
    return compas.value


def _parse_clave(clave: Clave, armadura: Armadura | None) -> str:
    """
    Combina la clave y la armadura en una expresión ABC.
    Actualmente, se mapea la clave de forma simplificada ignorando la armadura.
    """
    # Mapeo simple de claves musicales a notación ABC.
    clave_map = {
        Clave.SOL: "",
        Clave.FA:  "clef=bass",
        Clave.DO:  "clef=alto"
    }
    # Se obtiene la cadena correspondiente a la clave.
    if armadura:
        match armadura.tipo_modificacion:
            case ModificadorArmadura.BEMOL:
                notas_posibles = [
                "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"
                ]
            case ModificadorArmadura.SOSTENIDO:
                notas_posibles = [
                "G", "D", "A", "E", "B", "F#", "C#"
                ]
        clave_str = " ".join(notas_posibles[:armadura.cantidad_modificadores])
    else:
        clave_str = "C"
    return clave_map.get(clave, "") + clave_str


def _procesar_bloque(bloque_notas: list, context: tuple) -> str:
    """
    Recorre cada elemento del bloque de notas y devuelve su notación ABC correspondiente,
    teniendo en cuenta el contexto musical (clave, compás, armadura).
    """
    resultado = []
    clave_actual, compas_actual, armadura_actual = context

    for elemento in bloque_notas:
        if isinstance(elemento, Secuencia):
            resultado.append(_procesar_secuencia(elemento))
        elif isinstance(elemento, Repeticion):
            resultado.append(_procesar_repeticion(elemento))
        elif isinstance(elemento, Ligadura):
            resultado.append(_procesar_ligadura(elemento))
        elif isinstance(elemento, Fragmento):
            cambios = []
            nueva_clave = clave_actual
            nuevo_compas = compas_actual
            nueva_armadura = armadura_actual

            # Aplicar cambios de clave si están definidos en el fragmento
            if elemento.clave:
                nueva_clave = elemento.clave
                nueva_armadura = elemento.armadura
                cambios.append(f"K:{_parse_clave(elemento.clave, elemento.armadura)}")
            # Aplicar cambios de compás si están definidos en el fragmento
            if elemento.compas:
                nuevo_compas = elemento.compas
                cambios.append(f"M:{_parse_compas(elemento.compas)}")

            # Insertar un salto de línea antes de comenzar el fragmento si hay cambios
            if cambios:
                resultado.append("".join(cambios) + "\n")

            nuevo_contexto = (nueva_clave, nuevo_compas, nueva_armadura)
            # Procesar recursivamente el bloque interno del fragmento y añadir un salto de línea al final
            resultado.append(_procesar_bloque(elemento.bloque_notas, nuevo_contexto) + "\n")

            reversiones = []
            # Preparar reversiones al finalizar el fragmento
            if elemento.clave:
                reversiones.append(f"K:{_parse_clave(clave_actual, armadura_actual)}")
            if elemento.compas:
                reversiones.append(f"M:{_parse_compas(compas_actual)}")
            # Insertar un salto de línea al revertir cambios
            if reversiones:
                resultado.append("".join(reversiones) + "\n")
                
    return " ".join(resultado)

def _elemento_es_nota(elemento:str)->bool:
    notas = [
        "C", "D", "E", "F", "G", "A", "B", "Z"
    ]
    return any(n in elemento.upper() for n in notas)

def _valor_duracion(elemento:str)->float:
    nums = re.findall(r'\d+', elemento)
    if not nums:
        return 1.0
    numerador = int(nums[0])
    denominador = int(nums[1]) if len(nums) > 1 else 1
    return numerador/denominador

def _generar_silencios(decimal):
    fraccion = Fraction(decimal).limit_denominator(32)
    if fraccion.numerator == 3:
        return f"z{fraccion}"
    if fraccion.numerator > fraccion.denominator:
        partes = []
        while fraccion.numerator > fraccion.denominator:
            partes.append(f"z1")
            fraccion -= Fraction(fraccion.denominator, fraccion.denominator)
        if fraccion.numerator > 0:
            partes.append(f"z{fraccion}")
        return " ".join(partes)
    return f"z{fraccion}"

def _generar_lineas_divisorias(abc_cuerpo:str, obra_compas:Compas)-> str:
    pulsos = int(obra_compas.value.split("/")[0])
    pulsos_restantes:float = pulsos
    new_abc_cuerpo =''

    for linea in abc_cuerpo.split("\n"):
        if linea.startswith('M:'):
            pulsos =  int(linea.split(":")[1].split("/")[0])
            pulsos_restantes = pulsos
            new_abc_cuerpo += linea + "\n"
        elif linea.startswith('K:'):
            new_abc_cuerpo += linea + "\n"
        else:
            for elemento in linea.split(" "): # es un bloque?
                if not _elemento_es_nota(elemento):
                    if elemento == '|:' or elemento == ':|':
                        if pulsos_restantes != pulsos:
                            new_abc_cuerpo += f"{_generar_silencios(pulsos_restantes)} " 
                            pulsos_restantes = pulsos
                            new_abc_cuerpo += elemento + " "
                        else:
                            if elemento == '|:':
                                new_abc_cuerpo = new_abc_cuerpo.rstrip() + ":" + " "
                            else:
                                new_abc_cuerpo = new_abc_cuerpo[:-2] + ":|" + " "                            
                    continue
                #si es nota, coger numeros del elemento, que es la duracion
                valor_nota = _valor_duracion(elemento)
                if valor_nota > pulsos:
                    valor_nota = pulsos_restantes
                    
                if pulsos_restantes - valor_nota < 0: # nota no cabe en compas
                    new_abc_cuerpo += f"{_generar_silencios(pulsos_restantes)} | "
                    pulsos_restantes = pulsos
                if pulsos_restantes - valor_nota == 0: # justo
                    new_abc_cuerpo += f"{elemento} | "
                    pulsos_restantes = pulsos
                else: # nota cabe en compas
                    new_abc_cuerpo += elemento + " "
                    pulsos_restantes -= valor_nota
            new_abc_cuerpo += "\n"
    return new_abc_cuerpo

def generar_abc(obra: Obra) -> str:
    """
    Genera un string en notación ABC a partir de una instancia de Obra.
    Incluye encabezado y cuerpo procesado con gestión contextual.
    """
    # Construir las líneas de encabezado de la notación ABC.
    abc_lines = [
        "X:1",  # Número de referencia asigna 1
        f"T:{obra.nombre}",  # Título de la obra
        f"M:{_parse_compas(obra.compas)}",  # Compás de la obra
        f"K:{_parse_clave(obra.clave, obra.armadura)}",  # Clave y armadura de la obra
        "L:1/4",  # Forzar valor referencia notas a negra
    ]
    contexto_inicial = (obra.clave, obra.compas, obra.armadura)
    abc_cuerpo = _procesar_bloque(obra.bloque_notas, contexto_inicial)
    abc_cuerpo = _generar_lineas_divisorias(abc_cuerpo, obra.compas)
    abc_lines.append(abc_cuerpo)
    return "\n".join(abc_lines)
