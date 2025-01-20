"""Módulo para construir el proyecto con Antlr4."""

import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class AntlrBuilder(BuildHookInterface):
    def initialize(self, version, build_data):
        subprocess.run(
            [
                "antlr4",
                "-Dlanguage=Python3",
                "-Xexact-output-dir",
                "-o",
                "src/main/python/partitune/analysis/",
                "src/main/antlr/partitune/analysis/Scanner.g4",
            ],
            check=True,
        )
        subprocess.run(
            [
                "antlr4",
                "-Dlanguage=Python3",
                "-visitor",
                "-no-listener",
                "-lib",
                "src/main/python/partitune/analysis/",
                "-Xexact-output-dir",
                "-o",
                "src/main/python/partitune/analysis/",
                "src/main/antlr/partitune/analysis/Parser.g4",
            ],
            check=True,
        )
