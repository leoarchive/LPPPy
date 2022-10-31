#
# This file is part of the LPPPy distribution (https://github.com/leozamboni/LPPPy).
# Copyright (c) 2022 Leonardo Z. N.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from .lex import Lexer
from .parser import Parser
from .code import CodeGen
from .symtab import Symtab
import timeit
from datetime import datetime


class Compiler:
    startTime = timeit.default_timer()
    stdin = ""
    stdout = ""
    lexer = None
    parser = None
    codegen = None
    symtab = None

    def __init__(self, stdin):
        self.stdin = stdin
        self.symtab = Symtab()
        self.lexer = Lexer(stdin)
        self.parser = Parser(self.lexer, self.symtab)
        self.codegen = CodeGen(self.symtab)

    def run(self):
        self.parser.run()
        self.codegen.run(self.parser.tokens)
        header = """# coding: utf-8
# +-------------------------------------------------------+
#  Gerado por LPPPy (https://github.com/leozamboni/LPPPy).
#           ┌─────────────┬─────────────────────┐
#           │ Comp. date  │ %s │
#           ├─────────────┼─────────────────────┤
#           │ Comp. time  │ %.10f s.     │
#           └─────────────┴─────────────────────┘
# +-------------------------------------------------------+
""" % (
            datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            timeit.default_timer() - self.startTime,
        )
        self.stdout = header 
        self.stdout += f"# programa {self.codegen.programName}\n"
        self.stdout += self.codegen.stdout
