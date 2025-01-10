from typing import Optional
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

        clave: Optional[Clave] = claves[-1] if claves else None
        compas: Optional[Compas] = compases[-1] if compases else None
        armadura: Optional[Armadura] = armaduras[-1] if armaduras else None

        return clave, compas, armadura

    def visitPartitura(self, ctx: Parser.PartituraContext) -> ObraFinal:
        dict_fragmentos: dict[str, FragmentoSemantico] = {
            fragmento.nombre: fragmento
            for fragmento in map(
                lambda fragmento: self.visitFragmento(fragmento), ctx.fragmento()
            )
        }

        # TODO: sustituir str de fragmento.bloque_notas por Fragmento y cambiar tipo a FragmentoFinal

        obra: ObraSemantica = self.visitObra(ctx.obra())

        # TODO: sustituir str de obra.bloque_notas por Obra y cambiar tipo a ObraFinal

        return ObraSemantica

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
            raise ValueError(
                "No se pueden mezclar bemoles y sostenidos en una armadura"
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
