from lpppy.compiler.lex import Lexer
from lpppy.compiler.parse import Parse
from lpppy.compiler.code import CodeGen
from lpppy.compiler.symtab import Symtab
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

    def __init__(self, stdin: str) -> None:
        self.stdin = stdin
        self.symtab = Symtab()
        self.lexer = Lexer(stdin)
        self.parser = Parse(self.lexer, self.symtab)
        self.codegen = CodeGen(self.symtab)

    def run(self) -> None:
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
