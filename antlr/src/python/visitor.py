from typing import Optional
from networkx import DiGraph
from networkx.algorithms.cycles import simple_cycles
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


class Visitor(ParserVisitor):
    def __init__(self):
        super().__init__()
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def _obtener_especificacion(
        self, ctx: Parser.ObraContext | Parser.FragmentoContext
    ) -> tuple[Optional[Clave], Optional[Compas], Optional[Armadura]]:
        especificacion: list[Clave | Compas | Armadura] = list(
            map(
                lambda especificacion: self.visitEspecificacion(especificacion),
                ctx.especificacion(),
            )
        )

        claves: list[Clave] = list(
            filter(lambda x: isinstance(x, Clave), especificacion)
        )
        compases: list[Compas] = list(
            filter(lambda x: isinstance(x, Compas), especificacion)
        )
        armaduras: list[Armadura] = list(
            filter(lambda x: isinstance(x, Armadura), especificacion)
        )

        for clave in claves[1:]:
            self.warnings.append(
                f"Warning: clave duplicada en {ctx.especificacion(0).start.line}:{ctx.especificacion(0).start.column}"
            )
        for compas in compases[1:]:
            self.warnings.append(
                f"Warning: compás duplicado en {ctx.especificacion(0).start.line}:{ctx.especificacion(0).start.column}"
            )
        for armadura in armaduras[1:]:
            self.warnings.append(
                f"Warning: armadura duplicada en {ctx.especificacion(0).start.line}:{ctx.especificacion(0).start.column}"
            )

        clave: Optional[Clave] = claves[-1] if claves else None
        compas: Optional[Compas] = compases[-1] if compases else None
        armadura: Optional[Armadura] = armaduras[-1] if armaduras else None

        return clave, compas, armadura

    def _check_call_graph(
        self, fragmentos: dict[str, FragmentoSemantico], obra: ObraSemantica
    ) -> None:
        grafo_llamadas: DiGraph = DiGraph()
        grafo_llamadas.add_node(obra.nombre)

        for fragmento in fragmentos:
            grafo_llamadas.add_node(fragmento)

        for llamadas in filter(
            lambda elemento: isinstance(elemento, FragmentoLlamado), obra.bloque_notas
        ):
            if llamadas.nombre.upper() not in fragmentos:
                self.errors.append(
                    f"{llamadas.linea}:{llamadas.columna}: Fragmento '{llamadas.nombre}' no definido"
                )
            grafo_llamadas.add_edge(obra.nombre, llamadas.nombre.upper())

        for nombre, fragmento in fragmentos.items():
            for llamada in filter(
                lambda elemento: isinstance(elemento, FragmentoLlamado),
                fragmento.bloque_notas,
            ):
                if llamada.nombre.upper() not in fragmentos:
                    self.errors.append(
                        f"{llamada.linea}:{llamada.columna}: Fragmento '{llamada.nombre}' no definido"
                    )
                grafo_llamadas.add_edge(nombre, llamada.nombre.upper())

        for ciclo in simple_cycles(grafo_llamadas):
            self.errors.append(
                f"Error: Ciclo en llamadas de fragmentos: {' -> '.join(ciclo + [ciclo[0]])}"
            )

    def visitPartitura(self, ctx: Parser.PartituraContext) -> ObraFinal:
        fragmentos: list[FragmentoSemantico] = list(
            map(lambda fragmento: self.visitFragmento(fragmento), ctx.fragmento())
        )

        for i, fragmento in enumerate(fragmentos):
            for otro_fragmento in fragmentos[i + 1 :]:
                if fragmento == otro_fragmento:
                    self.errors.append(
                        f"{otro_fragmento.linea}:{otro_fragmento.columna}: Fragmento duplicado '{fragmento.nombre}'"
                    )

        obra: ObraSemantica = self.visitObra(ctx.obra())

        dict_fragmentos: dict[str, FragmentoSemantico] = {
            fragmento.nombre.upper(): fragmento for fragmento in fragmentos
        }

        self._check_call_graph(dict_fragmentos, obra)

        if self.errors:
            raise ValueError("\n".join(self.errors) + "\n" + "\n".join(self.warnings))

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
        nombre: str = ctx.TITULO().getText()

        clave, compas, armadura = self._obtener_especificacion(ctx)

        return ObraSemantica(
            nombre=nombre,
            bloque_notas=self.visitBloque_notas(ctx.bloque_notas()),
            clave=clave,
            compas=compas,
            armadura=armadura,
        )

    def visitClave(self, ctx: Parser.ClaveContext) -> Clave:
        return get_clave_from_partitune(ctx.NOTA_BASE().getText())

    def visitCompas(self, ctx: Parser.CompasContext) -> Compas:
        return get_compas_from_partitune(ctx.COMPAS_DURACION().getText())

    def visitArmadura(self, ctx: Parser.ArmaduraContext) -> Armadura:
        notas_armadura: list[tuple[ModificadorArmadura, NotaBase]] = list(
            map(
                lambda nota_armadura: self.visitNota_armadura(nota_armadura),
                ctx.nota_armadura(),
            )
        )
        hay_bemoles: bool = any(
            map(lambda x: x[0] == Modificador.BEMOL, notas_armadura)
        )
        hay_sostenidos: bool = any(
            map(lambda x: x[0] == ModificadorArmadura.SOSTENIDO, notas_armadura)
        )

        if hay_bemoles and hay_sostenidos:
            self.errors.append(
                f"{ctx.nota_armadura(0).start.line}:{ctx.nota_armadura(0).start.column}: No se pueden mezclar bemoles y sostenidos en una armadura"
            )

        notas_base: list[NotaBase] = list(map(lambda x: x[1], notas_armadura))

        return Armadura(
            tipo_modificacion=(
                ModificadorArmadura.BEMOL
                if hay_bemoles
                else ModificadorArmadura.SOSTENIDO
            ),
            notas=notas_base,
        )

    def visitNota_armadura(
        self, ctx: Parser.Nota_armaduraContext
    ) -> tuple[ModificadorArmadura, NotaBase]:
        modificador_armadura: ModificadorArmadura = (
            Modificador.BEMOL if ctx.BEMOL() else ModificadorArmadura.SOSTENIDO
        )
        nota_base: NotaBase = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())

        return modificador_armadura, nota_base

    def visitFragmento(self, ctx: Parser.FragmentoContext) -> FragmentoSemantico:
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

    def visitBloque_notas(
        self, ctx: Parser.Bloque_notasContext
    ) -> list[Secuencia | FragmentoLlamado | Repeticion | Ligadura]:
        return list(map(lambda elemento: self.visitElemento(elemento), ctx.elemento()))

    def visitRepeticion(self, ctx: Parser.RepeticionContext) -> Repeticion:
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

    def visitLigadura(self, ctx: Parser.LigaduraContext) -> Ligadura:
        return Ligadura(
            secuencias=list(
                map(lambda secuencia: self.visitSecuencia(secuencia), ctx.secuencia())
            )
        )

    def visitLlamada(self, ctx: Parser.LlamadaContext) -> FragmentoLlamado:
        return FragmentoLlamado(
            nombre=ctx.ID().getText(), linea=ctx.start.line, columna=ctx.start.column
        )

    def visitSecuencia(self, ctx: Parser.SecuenciaContext):
        duracion: Duracion = get_duracion_from_partitune(ctx.DURACION().getText())
        lista_notas: list[Nota | None] = list(
            map(
                lambda posibles_notas: self.visitPosibles_notas(posibles_notas),
                ctx.posibles_notas(),
            )
        )

        return Secuencia(duracion=duracion, lista_notas=lista_notas)

    def visitPosibles_notas(self, ctx: Parser.Posibles_notasContext) -> Nota | None:
        return self.visitNota(ctx.nota()) if ctx.nota() else None

    def visitModificador(self, ctx: Parser.ModificadorContext) -> Modificador:
        return (
            Modificador.BEMOL
            if ctx.BEMOL()
            else Modificador.SOSTENIDO if ctx.SOSTENIDO() else Modificador.BECUADRO
        )

    def visitNota(self, ctx: Parser.NotaContext) -> Nota:
        nota_base: NotaBase = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())
        modificador: Optional[Modificador] = (
            self.visitModificador(ctx.modificador()) if ctx.modificador() else None
        )
        octava: Optional[Octava] = (
            get_octava_from_partitune(ctx.OCTAVA().getText())
            if ctx.OCTAVA()
            else Octava.NORMAL
        )
        puntillo: bool = ctx.PUNTILLO() is not None

        return Nota(
            nota_base=nota_base,
            modificador=modificador,
            octava=octava,
            puntillo=puntillo,
        )
