from .analysis.ParserListener import ParserListener
from .analysis.Parser import Parser

from .partitune.octava import Octava, get_octava_from_partitune
from .partitune.nota_base import NotaBase, get_nota_base_from_partitune


class Listener(ParserListener):

    def __init__(self):
        self.id_table: dict[str, "type"] = {}
        self.abc: str = ""
        self.current_index = 1
        self.current_compas = None
        self.current_clave = None

    def exitNotas_armadura(self, ctx: Parser.Notas_armaduraContext):
        nro_bemoles: int = len(ctx.BEMOL())
        nro_sostenidos: int = len(ctx.SOSTENIDO())

        # FIXME: Pueden tener octava???
        notas_base: list[NotaBase] = list(
            map(
                lambda nota: get_nota_base_from_partitune(nota.getText()),
                ctx.NOTA_BASE(),
            )
        )

    def exitNota(self, ctx: Parser.NotaContext):
        octava: Octava = (
            Octava.NORMAL
            if ctx.OCTAVA() is None
            else get_octava_from_partitune(ctx.OCTAVA().getText())
        )
        nota_base: NotaBase = get_nota_base_from_partitune(ctx.NOTA_BASE().getText())

