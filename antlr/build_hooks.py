import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class AntlrBuilder(BuildHookInterface):
    def initialize(self, version, build_data):
        flags = [
            "antlr4",
            "-Dlanguage=Python3",
            "-lib",
            "src/python/analysis/",
            "-Xexact-output-dir",
            "-o",
            "src/python/analysis/",
        ]
        for src in ["Scanner.g4", "Parser.g4"]:
            subprocess.run(
                flags
                + [
                    f"src/antlr/{src}",
                ],
                check=True,
            )
