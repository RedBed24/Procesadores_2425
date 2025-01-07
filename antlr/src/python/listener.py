from .analysis.ParserListener import ParserListener
from .analysis.Parser import Parser
from .partitune.octava import Octava, get_octava_from_partitune
from .partitune.nota_base import get_nota_base_from_partitune
from .partitune.compas import get_compas_from_partitune
from .partitune.secuencia import Secuencia
from .partitune.clave import get_clave_from_partitune
from .partitune.obra import Obra
from .partitune.repeticion import Repeticion
from .partitune.ligadura import Ligadura
from .partitune.nota import Nota
from .partitune.duracion import get_duracion_from_partitune
from .partitune.modificador import get_modificador_from_partitune
from .partitune.tipo_repeticion import TipoRepeticion
from .partitune.fragmento import Fragmento


class Listener(ParserListener):
    """
    Listener para convertir un árbol de parseo en una instancia de Obra,
    construyendo secuencias, repeticiones, ligaduras y manejando fragmentos.
    """
    def __init__(self):
        self.obra = Obra(nombre="Sin título", bloque_notas=[])
        self.fragmentos: dict[str, Fragmento] = {}
        # Indicadores para saber si estamos dentro de una ligadura o repetición
        self.inside_ligadura = False
        self.inside_repeticion = False
        # Pila que indica el bloque actual en el que se van agregando los elementos
        # Inicialmente apunta al bloque de notas principal de la obra
        self.block_stack = [self.obra.bloque_notas]

    def exitObra(self, ctx: Parser.ObraContext):
        titulo = ctx.TITULO().getText().strip('"')
        self.obra.nombre = titulo  # Asignamos el título a la obra

        # Iteramos sobre cada especificación encontrada dentro de la obra
        for especificacion in ctx.especificacion():
            if especificacion.clave():
                # Si hay una clave especificada, la obtenemos y la asignamos a la obra
                clave = especificacion.clave().NOTA_BASE().getText()
                self.obra.clave = get_clave_from_partitune(clave)
            if especificacion.compas():
                # Si hay un compás especificado, lo obtenemos y lo asignamos a la obra
                compas = especificacion.compas().COMPAS_DURACION().getText()
                self.obra.compas = get_compas_from_partitune(compas)
            # Manejar armadura en la obra
         

    def enterFragmento(self, ctx: Parser.FragmentoContext):
        nombre = ctx.ID().getText().lower()
        fragmento = Fragmento(nombre=nombre, clave=None, armadura=None, compas=None)
        # Inicializamos la lista de notas del fragmento como vacía
        fragmento.bloque_notas = []

        # Procesamos cada especificación dentro del fragmento
        for espec in ctx.especificacion():
            if espec.clave():
                # Si se especifica una clave, la asignamos al fragmento
                fragmento.clave = get_clave_from_partitune(espec.clave().NOTA_BASE().getText())
            if espec.compas():
                # Si se especifica un compás, lo asignamos al fragmento
                fragmento.compas = get_compas_from_partitune(espec.compas().COMPAS_DURACION().getText())
            # Manejar armadura en el fragmento
            

        # Almacenamos el fragmento en el diccionario para poder referenciarlo luego
        self.fragmentos[nombre] = fragmento
        # Cambiamos el bloque de destino al bloque de notas del fragmento actual
        self.block_stack.append(fragmento.bloque_notas)

    def exitFragmento(self, ctx: Parser.FragmentoContext):
        # Al finalizar la definición de un fragmento, regresamos al bloque de notas anterior
        self.block_stack.pop()

    def exitLlamada(self, ctx: Parser.LlamadaContext):
        """
        Maneja una llamada a fragmento identificada por un ID.
        Busca el fragmento almacenado y expande su contenido en el bloque actual.
        """
        # Obtenemos el nombre del fragmento llamado y lo convertimos a minúsculas
        nombre = ctx.ID().getText().lower()
        # Buscamos el fragmento en el diccionario
        fragmento = self.fragmentos.get(nombre)
        if fragmento:
            self.block_stack[-1].append(fragmento)
        else:
            # Si el fragmento no está definido, mostramos una advertencia
            print(f"Advertencia: Fragmento '{nombre}' no definido.")

    def exitSecuencia(self, ctx: Parser.SecuenciaContext):
        """
        Procesa una secuencia de notas y la añade al bloque de notas actual,
        solo si no se encuentra dentro de una ligadura o repetición para evitar duplicados.
        """
        # Si estamos dentro de una ligadura o repetición, no procesamos la secuencia aquí
        if self.inside_ligadura or self.inside_repeticion:
            return

        # Obtenemos la duración de la secuencia actual desde el texto parseado
        duracion = get_duracion_from_partitune(ctx.DURACION().getText())
        lista_notas = []  

        # Iteramos sobre cada nota en la secuencia
        for nota_ctx in ctx.nota():
            if nota_ctx.getText() == '-':
                # '-', representa un silencio
                lista_notas.append(None)
            else:
                # Si no es un guión, procesamos la nota mediante el método exitNota
                lista_notas.append(self.exitNota(nota_ctx))

        # Creamos un objeto Secuencia con la duración y las notas obtenidas
        secuencia = Secuencia(duracion=duracion, lista_notas=lista_notas)
        # Añadimos la secuencia al bloque de notas actual apuntado por la cima de la pila
        self.block_stack[-1].append(secuencia)

    def exitNota(self, ctx: Parser.NotaContext) -> Nota:
        # Procesa un nodo Nota del árbol de parseo y crea un objeto Nota correspondiente

        # Obtenemos la nota base (do, re, mi, etc.) a partir del texto
        nota_base = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())
        # Verificamos si la nota tiene un modificador (sostenido, bemol, etc.) y lo obtenemos si existe
        modificador = get_modificador_from_partitune(ctx.modificador().getText()) if ctx.modificador() else None
        # Determinamos la octava de la nota; si no se especifica, usamos la octava normal
        octava = get_octava_from_partitune(ctx.OCTAVA().getText()) if ctx.OCTAVA() else Octava.NORMAL
        # Verificamos si la nota tiene puntillo (un punto que modifica la duración)
        puntillo = ctx.PUNTILLO() is not None

        # Retornamos una nueva instancia de Nota con todos los atributos especificados
        return Nota(
            nota_base=nota_base,
            modificador=modificador,
            octava=octava,
            puntillo=puntillo
        )

    def enterRepeticion(self, ctx: Parser.RepeticionContext):
        """
        Marca el inicio de un contexto de repetición.
        """
        # Establecemos el indicador de que estamos dentro de una repetición
        self.inside_repeticion = True
    
    def exitRepeticion(self, ctx: Parser.RepeticionContext):
        """
        Procesa una repetición de secuencias y la añade al bloque de notas actual,
        restableciendo el indicador de repetición al finalizar.
        """
        # Determinamos el tipo de repetición: con o sin señal de inicio
        tipo_repeticion = TipoRepeticion.CON_INICIO if ctx.PRINCIPIO_REP() else TipoRepeticion.SIN_INICIO
        lista_secuencias = []  # Lista para almacenar las secuencias dentro de la repetición

        # Iteramos sobre cada secuencia declarada dentro de la repetición
        for secuencia_ctx in ctx.secuencia():
            # Obtenemos la duración de la secuencia actual
            duracion = get_duracion_from_partitune(secuencia_ctx.DURACION().getText())
            lista_notas = []  # Lista para almacenar las notas de la secuencia actual

            # Iteramos sobre cada nota en la secuencia
            for nota_ctx in secuencia_ctx.nota():
                if nota_ctx.getText() == '-':
                    # Si la nota es un guión, agregamos None para indicar silencio
                    lista_notas.append(None)
                else:
                    # Si es una nota válida, la procesamos con exitNota
                    lista_notas.append(self.exitNota(nota_ctx))

            # Creamos una nueva secuencia con la duración y las notas procesadas
            secuencia = Secuencia(duracion=duracion, lista_notas=lista_notas)
            # Añadimos la secuencia a la lista de secuencias de la repetición
            lista_secuencias.append(secuencia)

        # Creamos un objeto Repeticion con el tipo y la lista de secuencias obtenidas
        repeticion = Repeticion(tipo_repeticion=tipo_repeticion, secuencias=lista_secuencias)
        # Añadimos la repetición al bloque de notas actual
        self.block_stack[-1].append(repeticion)
        # Restablecemos el indicador de repetición, ya que hemos salido del contexto
        self.inside_repeticion = False
        
    def enterLigadura(self, ctx: Parser.LigaduraContext):
        """
        Marca el inicio de un contexto de ligadura.
        """
        # Indicamos que estamos dentro de una ligadura
        self.inside_ligadura = True

    def exitLigadura(self, ctx: Parser.LigaduraContext):
        """
        Procesa una ligadura de secuencias y la añade al bloque de notas actual,
        restableciendo el indicador de ligadura al finalizar.
        """
        lista_secuencias = []  # Lista para almacenar las secuencias dentro de la ligadura

        # Iteramos sobre cada secuencia en la ligadura
        for secuencia_ctx in ctx.secuencia():
            # Obtenemos la duración de la secuencia actual
            duracion = get_duracion_from_partitune(secuencia_ctx.DURACION().getText())
            lista_notas = []  # Lista para almacenar las notas en la secuencia

            # Iteramos sobre cada nota de la secuencia
            for nota_ctx in secuencia_ctx.nota():
                if nota_ctx.getText() == '-':
                    # Si encontramos un guión, representa un silencio
                    lista_notas.append(None)
                else:
                    # Si es una nota, la procesamos normalmente
                    lista_notas.append(self.exitNota(nota_ctx))

            # Creamos una nueva secuencia con la duración y las notas obtenidas
            secuencia = Secuencia(duracion=duracion, lista_notas=lista_notas)
            # Añadimos la secuencia a la lista de secuencias de la ligadura
            lista_secuencias.append(secuencia)

        # Creamos un objeto Ligadura utilizando la lista de secuencias recolectadas
        ligadura = Ligadura(secuencias=lista_secuencias)
        # Añadimos la ligadura al bloque de notas actual
        self.block_stack[-1].append(ligadura)
        # Restablecemos el indicador de ligadura, pues hemos terminado de procesarla
        self.inside_ligadura = False
