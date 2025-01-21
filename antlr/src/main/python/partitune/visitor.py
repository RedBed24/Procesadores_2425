"""Modulo para el visitor"""
from typing import Optional
from networkx import DiGraph
from networkx.algorithms.cycles import simple_cycles
from networkx.algorithms.dag import descendants
from .analysis.ParserVisitor import ParserVisitor
from .analysis.Parser import Parser
from .partitune.armadura import Armadura, ModificadorArmadura
from .partitune.octava import Octava, get_octava_from_partitune
from .partitune.nota_base import NotaBase, get_nota_base_from_partitune
from .partitune.compas import Compas, get_compas_from_partitune
from .partitune.secuencia import Secuencia
from .partitune.clave import Clave, get_clave_from_partitune
from .partitune.obra import Obra, ObraSemantica, ObraFinal
from .partitune.repeticion import Repeticion
from .partitune.ligadura import Ligadura
from .partitune.nota import Nota
from .partitune.duracion import Duracion, get_duracion_from_partitune
from .partitune.modificador import Modificador
from .partitune.tipo_repeticion import TipoRepeticion
from .partitune.fragmento import (
    Fragmento,
    FragmentoLlamado,
    FragmentoSemantico,
    FragmentoFinal,
)
from .utils.errors import *


class Visitor(ParserVisitor):
    """Clase que implementa el visitor completo para Partitune"""
    def __init__(self, errores_anteriores: list[LexerError] = None):
        """Constructor de la clase
        
        :param errores_anteriores: Lista de errores anteriores."""
        super().__init__()
        # nos sirve recoger todos los posibles errores y lanzarlos al final
        self.errors: list[SemanticError | LexerError | ParserError] = errores_anteriores or []
        self.warnings: list[Warning] = []

    def _obtener_especificacion(
        self, ctx: Parser.ObraContext | Parser.FragmentoContext
    ) -> tuple[Optional[Clave], Optional[Compas], Optional[Armadura]]:
        """Obtiene la especificación de la obra o fragmento"""
        especificacion: list[Clave | Compas | Armadura] = list(
            filter(
                # eliminamos aquellas que hayan podido fallar
                lambda x: x is not None,
                map(
                    # por cada especificación, la visitamos
                    lambda especificacion: self.visitEspecificacion(especificacion),
                    ctx.especificacion(),
                ),
            )
        )

        # filtramos las claves, compases y armaduras
        claves: list[Clave] = list(
            filter(lambda x: isinstance(x, Clave), especificacion)
        )
        compases: list[Compas] = list(
            filter(lambda x: isinstance(x, Compas), especificacion)
        )
        armaduras: list[Armadura] = list(
            filter(lambda x: isinstance(x, Armadura), especificacion)
        )

        # si hay más de una clave, compás o armadura, lanzamos una advertencia
        for clave in claves[1:]:
            self.warnings.append(
                ClaveDuplicationWarning(
                    ctx.especificacion(0).start.line,
                    ctx.especificacion(0).start.column,
                    clave.value,
                )
            )
        for compas in compases[1:]:
            self.warnings.append(
                CompasDuplicationWarning(
                    ctx.especificacion(0).start.line,
                    ctx.especificacion(0).start.column,
                    compas.value,
                )
            )
        for armadura in armaduras[1:]:
            self.warnings.append(
                ArmaduraDuplicationWarning(
                    ctx.especificacion(0).start.line,
                    ctx.especificacion(0).start.column,
                    ctx.especificacion(0).getText(),
                )
            )

        # obtenemos la última clave, compás y armadura si es que hay
        clave: Optional[Clave] = claves[-1] if claves else None
        compas: Optional[Compas] = compases[-1] if compases else None
        armadura: Optional[Armadura] = armaduras[-1] if armaduras else None

        return clave, compas, armadura

    def _obtener_elementos(self, ctx: Parser.Bloque_notasContext | Parser.Error_repeticionContext | Parser.Error_ligaduraContext) -> list[Secuencia | FragmentoLlamado | Repeticion | Ligadura]:
        """Obtiene los elementos de un bloque de notas o de algún posible nodo de error"""
        elementos = list(
            filter(
                # eliminamos aquellas que hayan podido fallar
                lambda e: e,
                # por cada elemento, lo visitamos
                map(lambda elemento: self.visitElemento(elemento), ctx.elemento()),
            )
        )
        # si resulta que había una lista de estos elementos, la desempaquetamos
        # esto viene de un nodo de error
        listas = list(filter(lambda e: isinstance(e, list), elementos))
        return elementos + [elemento for lista in listas for elemento in lista]

    def _check_call_graph(
        self, fragmentos: dict[str, FragmentoSemantico], obra: ObraSemantica
    ) -> None:
        """Chequea el grafo de llamadas de los fragmentos en búsqueda de posibles errores"""
        # crearemos un grafo dirigido
        grafo_llamadas: DiGraph = DiGraph()
        # añadimos la obra como nodo
        grafo_llamadas.add_node(obra.nombre)

        # añadimos cada fragmento como nodo
        for fragmento in fragmentos:
            grafo_llamadas.add_node(fragmento)

        # añadimos las llamadas de la obra
        for llamada in filter(
            lambda elemento: isinstance(elemento, FragmentoLlamado), obra.bloque_notas
        ):
            # comprobamos si existe el fragmento llamado
            if llamada.nombre.upper() not in fragmentos:
                self.errors.append(
                    LlamadaNoDefinidaError(
                        llamada.linea, llamada.columna, llamada.nombre
                    )
                )
            # añadimos la llamada al grafo
            grafo_llamadas.add_edge(obra.nombre, llamada.nombre.upper())

        # por cada fragmento, añadimos las llamadas
        for nombre, fragmento in fragmentos.items():
            for llamada in filter(
                lambda elemento: isinstance(elemento, FragmentoLlamado),
                fragmento.bloque_notas,
            ):
                if llamada.nombre.upper() not in fragmentos:
                    self.errors.append(
                        LlamadaNoDefinidaError(
                            llamada.linea, llamada.columna, llamada.nombre
                        )
                    )
                grafo_llamadas.add_edge(nombre, llamada.nombre.upper())

        # comprobamos si hay ciclos
        for ciclo in simple_cycles(grafo_llamadas):
            self.errors.append(LlamadaCircularError(ciclo + [ciclo[0]]))

        # comprobamos si hay fragmentos no usados
        fragmentos_usados = descendants(grafo_llamadas, obra.nombre)

        # por cada fragmento, nos quedamos con aquellos que no han sido usados
        for nombre, fragmento in filter(
            lambda x: x[0] not in fragmentos_usados, fragmentos.items()
        ):
            self.warnings.append(
                FragmentoNoUsadoWarning(fragmento.linea, fragmento.columna, nombre)
            )

    def visitPartitura(self, ctx: Parser.PartituraContext) -> ObraFinal:
        """Visita la partitura, cargando todos los datos correspondientes"""
        try:
            fragmentos: list[FragmentoSemantico] = list(
                map(lambda fragmento: self.visitFragmento(fragmento), ctx.fragmento())
            )

            obra: ObraSemantica = self.visitObra(ctx.obra())

            # por cada fragmento, comprobamos si hay duplicados
            for i, fragmento in enumerate(fragmentos):
                for otro_fragmento in fragmentos[i + 1 :]:
                    if fragmento == otro_fragmento:
                        self.errors.append(
                            FragmentoDuplicationError(
                                otro_fragmento.linea,
                                otro_fragmento.columna,
                                fragmento.nombre,
                            )
                        )

            dict_fragmentos: dict[str, FragmentoSemantico] = {
                fragmento.nombre.upper(): fragmento for fragmento in fragmentos
            }

            self._check_call_graph(dict_fragmentos, obra)
        except AttributeError as e:
            raise PartituneError(self.errors, self.warnings) from e

        if self.errors:
            raise PartituneError(self.errors, self.warnings)

        # convertimos las llamadas a fragmentos finales, haciendo que tengan todos los atributos
        for fragmento in dict_fragmentos.values():
            fragmento.bloque_notas = list(
                map(
                    lambda elemento: (
                        dict_fragmentos[elemento.nombre.upper()]
                        if isinstance(elemento, FragmentoLlamado)
                        else elemento
                    ),
                    fragmento.bloque_notas,
                )
            )

        obra.bloque_notas = list(
            map(
                lambda elemento: (
                    dict_fragmentos[elemento.nombre.upper()]
                    if isinstance(elemento, FragmentoLlamado)
                    else elemento
                ),
                obra.bloque_notas,
            )
        )

        return obra

    def visitObra(self, ctx: Parser.ObraContext) -> ObraSemantica:
        """Visita la obra, cargando todos los datos correspondientes y creando
        la obra con los datos obtenidos"""
        if ctx.error_obra():
            # en caso de haber obra, visitamos la obra
            return self.visitError_obra(ctx.error_obra())
        nombre: str = ctx.TITULO().getText()

        clave, compas, armadura = self._obtener_especificacion(ctx)

        return ObraSemantica(
            nombre=nombre,
            bloque_notas=self.visitBloque_notas(ctx.bloque_notas()),
            clave=clave,
            compas=compas,
            armadura=armadura,
        )

    def visitError_obra(self, ctx:Parser.Error_obraContext) -> ObraSemantica:
        """Visita la obra, cargando todos los datos correspondientes y creando
        la obra con los datos obtenidos"""
        # lanzamos un error genérico, indicando que se esperaba un ID o un TITULO
        self.errors.append(
            GenericParserError(
                ctx.start.line,
                ctx.start.column,
                Parser.RULE_obra,
                Parser.ID if ctx.ID() else Parser.TITULO,
                ctx.ID().getText() if ctx.ID() else ctx.TITULO().getText(),
                [Parser.OBRA],
                ctx,
            )
        )
        nombre: str = ctx.TITULO().getText()

        clave, compas, armadura = self._obtener_especificacion(ctx)

        return ObraSemantica(
            nombre=nombre,
            bloque_notas=self.visitBloque_notas(ctx.bloque_notas()),
            clave=clave,
            compas=compas,
            armadura=armadura,
        )

    def visitError_especificacion(self, ctx: Parser.Error_especificacionContext) -> None:
        self.errors.append(
            GenericParserError(
                ctx.start.line,
                ctx.start.column,
                Parser.RULE_especificacion,
                Parser.ID,
                ctx.ID().getText(),
                [Parser.CLAVE, Parser.COMPAS, Parser.ARMADURA],
                ctx,
            )
        )
        return None

    def visitClave(self, ctx: Parser.ClaveContext) -> Clave | None:
        """Visita la clave, obteniendo la clave correspondiente si no ha habido errores"""
        try:
            return get_clave_from_partitune(ctx.NOTA_BASE().getText())
        except ValueError as e:
            # en caso de error, lanzamos un error de clave y devolvemos None
            # esto es factible porque la clave es opcional
            self.errors.append(NotaClaveError(ctx.start.line, ctx.start.column, str(e)))
            return None

    def visitCompas(self, ctx: Parser.CompasContext) -> Compas:
        """Visita el compás, obteniendo el compás correspondiente"""
        # obtenemos el compás a partir del texto
        return get_compas_from_partitune(ctx.COMPAS_DURACION().getText())

    def visitArmadura(self, ctx: Parser.ArmaduraContext) -> Armadura | None:
        """Visita la armadura, obteniendo la armadura correspondiente"""
        # obtenemos la lista de notas con sus modificadores
        notas_armadura: list[tuple[ModificadorArmadura, NotaBase]] = list(
            map(
                lambda nota_armadura: self.visitNota_armadura(nota_armadura),
                ctx.nota_armadura(),
            )
        )
        # comprobamos si hay bemoles y sostenidos
        hay_bemoles: bool = any(
            map(lambda x: x[0] == Modificador.BEMOL, notas_armadura)
        )
        hay_sostenidos: bool = any(
            map(lambda x: x[0] == ModificadorArmadura.SOSTENIDO, notas_armadura)
        )

        if hay_bemoles and hay_sostenidos:
            self.errors.append(
                ModificadorArmaduraError(
                    ctx.nota_armadura(0).start.line, ctx.nota_armadura(0).start.column
                )
            )

        notas_base: list[NotaBase] = list(map(lambda x: x[1], notas_armadura))

        try:
            # intentamos crear la armadura y devolverla
            return Armadura(
                tipo_modificacion=(
                    ModificadorArmadura.BEMOL # asumimos que hay bemoles en caso de error
                    if hay_bemoles
                    else ModificadorArmadura.SOSTENIDO
                ),
                notas=notas_base,
            )
        except ValueError as e:
            # si ha habido error de armadura, lanzamos un error y devolvemos None
            self.errors.append(
                NotasArmaduraError(
                    ctx.nota_armadura(0).start.line,
                    ctx.nota_armadura(0).start.column,
                    notas_base,
                )
            )
            return None

    def visitNota_armadura(
        self, ctx: Parser.Nota_armaduraContext
    ) -> tuple[ModificadorArmadura, NotaBase]:
        """Visita la nota de la armadura, obteniendo el modificador y la nota base"""
        # comprobamos el modificador
        modificador_armadura: ModificadorArmadura = (
            Modificador.BEMOL if ctx.BEMOL() else ModificadorArmadura.SOSTENIDO
        )
        # obtenemos la nota base a partir del texto
        nota_base: NotaBase = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())

        return modificador_armadura, nota_base

    def visitFragmento(self, ctx: Parser.FragmentoContext) -> FragmentoSemantico:
        if ctx.error_fragmento():
            return self.visitError_fragmento(ctx.error_fragmento())
        nombre: str = ctx.ID().getText()

        clave, compas, armadura = self._obtener_especificacion(ctx)

        return FragmentoSemantico(
            nombre=nombre,
            bloque_notas=self.visitBloque_notas(ctx.bloque_notas()),
            linea=ctx.start.line,
            columna=ctx.start.column,
            clave=clave,
            compas=compas,
            armadura=armadura,
        )

    def visitError_fragmento(self, ctx:Parser.Error_fragmentoContext) -> FragmentoSemantico:
        self.errors.append(
            GenericParserError(
                ctx.start.line,
                ctx.start.column,
                Parser.RULE_fragmento,
                Parser.ID,
                ctx.ID(0).getText(),
                [Parser.FRAGMENTO],
                ctx,
            )
        )
        nombre: str = ctx.ID(len(ctx.ID())-1).getText()

        clave, compas, armadura = self._obtener_especificacion(ctx)

        return FragmentoSemantico(
            nombre=nombre,
            bloque_notas=self.visitBloque_notas(ctx.bloque_notas()),
            linea=ctx.start.line,
            columna=ctx.start.column,
            clave=clave,
            compas=compas,
            armadura=armadura,
        )


    def visitBloque_notas(
        self, ctx: Parser.Bloque_notasContext
    ) -> list[Secuencia | FragmentoLlamado | Repeticion | Ligadura]:
        """Visita el bloque de notas, obteniendo todos los elementos del bloque"""
        return self._obtener_elementos(ctx)

    def visitRepeticion(self, ctx: Parser.RepeticionContext) -> Repeticion | list[FragmentoLlamado]:
        if ctx.error_repeticion():
            return self.visitError_repeticion(ctx.error_repeticion())
        tipo_repeticion: TipoRepeticion = (
            TipoRepeticion.CON_INICIO
            if ctx.PRINCIPIO_REP()
            else TipoRepeticion.SIN_INICIO
        )
        return Repeticion(
            tipo_repeticion=tipo_repeticion,
            secuencias=list(
                map(lambda secuencia: self.visitSecuencia(secuencia), ctx.secuencia())
            ),
        )

    def visitError_repeticion(self, ctx:Parser.Error_repeticionContext) -> list[FragmentoLlamado]:
        self.errors.append(
            RepeticionError(ctx.start.line, ctx.start.column, ctx.stop.line, ctx.stop.column, ctx)
        )
        # estamos en un error, nos quedamos sólo con lo interesante, las llamadas
        # aunque igualmente, visitamos todos los elementos para comprobar si hay errores
        return filter(lambda e: isinstance(e, FragmentoLlamado), self._obtener_elementos(ctx))
        
    def visitLigadura(self, ctx: Parser.LigaduraContext) -> Ligadura | None | list[FragmentoLlamado]:
        """Visita la ligadura, obteniendo la ligadura correspondiente

        :param ctx: Contexto de la ligadura

        :return: Ligadura correspondiente en caso de éxito, None en caso de ligadura con silencios o con una nota,
                 o una lista de llamadas en caso de tener elementos dentro
        """
        if ctx.error_ligadura():
            return self.visitError_ligadura(ctx.error_ligadura())
        try:
            return Ligadura(
                secuencias=list(
                    map(
                        lambda secuencia: self.visitSecuencia(secuencia),
                        ctx.secuencia(),
                    )
                )
            )
        except ValueError as e:
            self.errors.append(LigaduraSilencioError(ctx.start.line, ctx.start.column))
            return None
        except AttributeError as e:
            self.errors.append(LigaduraNotasError(ctx.start.line, ctx.start.column))
            return None

    def visitError_ligadura(self, ctx:Parser.Error_ligaduraContext) -> list[FragmentoLlamado]:
        elementos = self._obtener_elementos(ctx)
        if any(not isinstance(e, Secuencia) for e in elementos):
            self.errors.append(
                LigaduraError(ctx.start.line, ctx.start.column, ctx.stop.line, ctx.stop.column, ctx)
            )
        if ctx.ID():
            self.errors.append(
                GenericParserError(
                    ctx.start.line,
                    ctx.start.column,
                    Parser.RULE_elemento,
                    Parser.ID,
                    ctx.ID().getText(),
                    [Parser.LIGADURA],
                    ctx,
                )
            )
        try:
            Ligadura(
                secuencias=list(
                    filter(lambda e: isinstance(e, Secuencia), elementos)
                ),
            )
        except ValueError as e:
            self.errors.append(LigaduraSilencioError(ctx.start.line, ctx.start.column))
        except AttributeError as e:
            self.errors.append(LigaduraNotasError(ctx.start.line, ctx.start.column))

        return filter(lambda e: isinstance(e, FragmentoLlamado), elementos)

    def visitLlamada(self, ctx: Parser.LlamadaContext) -> FragmentoLlamado:
        return FragmentoLlamado(
            nombre=ctx.ID().getText(), linea=ctx.start.line, columna=ctx.start.column
        )

    def visitSecuencia(self, ctx: Parser.SecuenciaContext):
        duracion: Duracion = get_duracion_from_partitune(ctx.DURACION().getText())
        lista_notas: list[Nota | None] = list(
            map(
                # no filtramos los none porque representan silencios
                lambda posibles_notas: self.visitPosibles_notas(posibles_notas),
                ctx.posibles_notas(),
            )
        )

        return Secuencia(duracion=duracion, lista_notas=lista_notas)

    def visitPosibles_notas(self, ctx: Parser.Posibles_notasContext) -> Nota | None:
        """Visita las posibles notas, obteniendo la nota o silencio correspondiente
        
        :param ctx: Contexto de las posibles notas

        :return: Nota correspondiente en caso de ser una nota, None en caso de ser un silencio
        """
        return self.visitNota(ctx.nota()) if ctx.nota() else None

    def visitModificador(self, ctx: Parser.ModificadorContext) -> Modificador:
        return (
            # la información del modificador la obtenemos a partir de los tokens
            # sólo nos interesa el tipo de modificador, que están en diferentes tokens
            Modificador.BEMOL
            if ctx.BEMOL()
            else Modificador.SOSTENIDO if ctx.SOSTENIDO() else Modificador.BECUADRO
        )

    def visitNota(self, ctx: Parser.NotaContext) -> Nota | None:
        """Visita la nota, obteniendo la nota correspondiente, visitamos todos los nodos
        extrayendo la información necesaria"""
        if ctx.error_nota():
            print("Error en la nota")
            return self.visitError_nota(ctx.error_nota())
        # la nota base tiene un atributo, que es el texto, y este nos interesa
        # para obtener la nota base que sea
        nota_base: NotaBase = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())
        modificador: Optional[Modificador] = (
            self.visitModificador(ctx.modificador()) if ctx.modificador() else None
        )
        octava: Optional[Octava] = (
            get_octava_from_partitune(ctx.OCTAVA().getText())
            if ctx.OCTAVA()
            else Octava.NORMAL
        )
        # la información que nos aporta el puntillo, es si hay puntillo o no
        # no tiene atributos
        puntillo: bool = ctx.PUNTILLO() is not None

        return Nota(
            nota_base=nota_base,
            modificador=modificador,
            octava=octava,
            puntillo=puntillo,
        )
    
    def visitError_nota(self, ctx:Parser.Error_notaContext) -> None:
        self.errors.append(
            GenericParserError(
                ctx.start.line,
                ctx.start.column,
                Parser.RULE_nota,
                Parser.ID,
                ctx.ID().getText(),
                [Parser.NOTA_BASE],
                ctx,
            )
        )
        return None
