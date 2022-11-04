from lpppy.compiler.symtab import Symtab
from lpppy.compiler.token import Token, TokenKeys, TokenTypes
from lpppy.compiler.error import Error, ErrorTypes


class CodeGen:
    symtab: Symtab = None
    tokens: list[Token] = []
    index: int = 0
    stdout: str = ""
    level: int = 0
    programName: str = ""

    def __init__(self, symtab: Symtab) -> None:
        self.symtab = symtab

    def run(self, tokens: list[Token]):
        self.tokens = tokens
        self.gen()

    def importLib(self, lib: str) -> None:
        stdout = self.stdout
        self.stdout = f"{lib}\n"
        self.stdout += stdout

    def getDType(self, key: str) -> str:
        if self.symtab.checkDType(key):
            return key

        match key:
            case TokenKeys.caractere:
                return "str"
            case TokenKeys.inteiro:
                return "int"
            case TokenKeys.real:
                return "float"
            case TokenKeys.logico:
                return "bool"
            case _: 
                return "None"

    def getAssigDType(self, key: str, size: int, matrix: bool, _keytype: str) -> str:
        if self.symtab.checkDType(key):
            return f"{key}()"

        match key:
            case TokenKeys.caractere:
                return "''"
            case TokenKeys.inteiro:
                return "0"
            case TokenKeys.real:
                return "0.0"
            case TokenKeys.logico:
                return "False"
            case TokenKeys.conjunto:
                match _keytype:
                    case TokenKeys.caractere:
                        if matrix and size:
                            return f"[['' for _ in range({size})] for _ in range({size})]"
                        elif size:
                            return f"[''] * {size}"
                        else:
                            return "['']"
                    case TokenKeys.inteiro | TokenKeys.logico:
                        if matrix and size:
                            return f"[[0 for _ in range({size})] for _ in range({size})]"
                        elif size:
                            return f"[0] * {size}"
                        else:
                            return "[0]"
                    case TokenKeys.real:
                        if matrix and size:
                            return f"[[0.0 for _ in range({size})] for _ in range({size})]"
                        elif size:
                            return f"[0.0] * {size}"
                        else:
                            return "[0.0]"
                    case _:
                        if matrix:
                            return f"[0][0]"
                        elif size:
                            return f"[] * {size}"
                        else:
                            return "[]"

    def getInputCast(self, key: str) -> str:
        type = self.symtab.getType(key)
        match type:
            case TokenKeys.inteiro:
                return "int(input())"
            case TokenKeys.real:
                return "float(input())"
            case _:
                return "input()"

    def getLogical(self, key: str) -> str:
        match key:
            case TokenKeys._and:
                return "and"
            case TokenKeys._not:
                return "not"
            case TokenKeys._or:
                return "or"
            case TokenKeys.NotEq:
                return "!="
            case TokenKeys.equal:
                return "=="
            case _:
                return key

    def getMath(self, key: str) -> str:
        if key == TokenKeys.exponent:
            return "**"
        else:
            return key

    def gen(self) -> None:
        self.programName = self.tokens[self.index].key
        self.index += 1

        if self.tokens[self.index].key == TokenKeys.tipo:
            self.genRegistro()

        while self.tokens[self.index].key == TokenKeys.procedimento:
            self.stdout += "\ndef "
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}():\n"
            self.index += 2
            self.level += 1
            self.genProcedimento()
            self.index += 1
            self.level -= 1

        while self.tokens[self.index].key == TokenKeys.funcao:
            self.stdout += "\ndef "
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}("
            self.index += 1
            self.index += 1

            while self.tokens[self.index].key != TokenKeys.rParen:
                self.stdout += self.tokens[self.index].key
                self.index += 1

                if self.tokens[self.index].type == TokenTypes.dType:
                    self.stdout += ": "
                    self.stdout += self.getDType(self.tokens[self.index].key)
                    self.index += 1

                if self.tokens[self.index].key == TokenKeys.comma:
                    self.stdout += ", "
                    self.index += 1

            self.stdout += ")"
            self.index += 2
            self.level += 1

            if self.tokens[self.index].type == TokenTypes.dType:
                self.stdout += f" -> {self.getDType(self.tokens[self.index].key)}:\n"
                self.index += 1
            else:
                self.stdout += f" -> None:\n"

            self.genProcedimento()
            self.index += 1
            self.level -= 1

        self.stdout += "\n# var\n"
        self.index += 1
        self.genVarBlock()

    def genRegistro(self) -> None:
        self.importLib("from dataclasses import dataclass")
        self.index += 1
        while self.tokens[self.index].type != TokenTypes.var:
            self.stdout += f"\n@dataclass\nclass {self.tokens[self.index].key}:\n"
            self.index += 3
            self.genRegistroBlock()
            self.index += 1

    def genRegistroBlock(self) -> None:
        while self.tokens[self.index].type != TokenTypes.fimreg:
            if self.tokens[self.index + 1].key == TokenKeys.conjunto:
                if self.tokens[self.index + 5].type == TokenTypes.comma:
                    self.stdout += f"\t{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key, True, self.tokens[self.index + 9].key)}\n"
                    self.index += 8
                else:
                    self.stdout += f"\t{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key, False, self.tokens[self.index + 6].key)}\n"
                    self.index += 5

            elif self.tokens[self.index + 1].key == TokenKeys.comma:
                contents = 1
                self.stdout += "\t"

                while True:
                    self.stdout += self.tokens[self.index].key
                    if self.tokens[self.index + 1].type == TokenTypes.dType:
                        self.index += 1
                        break
                    else:
                        contents += 1
                        self.stdout += ", "
                        self.index += 2

                if self.tokens[self.index].key == TokenKeys.conjunto:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, self.tokens[self.index + 3].key, False, self.tokens[self.index + 5].key)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index += 4

                else:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, 0, False, None)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += f"\t{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, 0, False, None)}\n"

            self.index += 2

    def genVarBlock(self) -> None:
        while self.tokens[self.index].type != TokenTypes.inicio:
            if self.tokens[self.index + 1].key == TokenKeys.conjunto:
                if self.tokens[self.index + 5].type == TokenTypes.comma:
                    self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key, True, self.tokens[self.index + 9].key)}\n"
                    self.index += 8
                else:
                    self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key, False, self.tokens[self.index + 6].key)}\n"
                    self.index += 5

            elif self.tokens[self.index + 1].key == TokenKeys.comma:
                contents = 1

                while True:
                    self.stdout += self.tokens[self.index].key
                    if self.tokens[self.index + 1].type == TokenTypes.dType:
                        self.index += 1
                        break
                    else:
                        contents += 1
                        self.stdout += ", "
                        self.index += 2

                if self.tokens[self.index].key == TokenKeys.conjunto:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, self.tokens[self.index + 3].key, False, self.tokens[self.index + 5].key)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index += 4

                else:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, 0, False, None)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, 0, False, None)}\n"

            self.index += 2

        self.genInicio()

    def genProcedimento(self) -> None:
        while self.tokens[self.index].type != TokenTypes.inicio:
            if self.tokens[self.index + 1].key == TokenKeys.conjunto:
                self.stdout += "\t"
                self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key, False, self.tokens[self.index + 6].key)}\n"
                self.index += 5

            elif self.tokens[self.index + 1].key == TokenKeys.comma:
                self.stdout += "\t"
                contents = 1

                while True:
                    self.stdout += self.tokens[self.index].key
                    if self.tokens[self.index + 1].type == TokenTypes.dType:
                        self.index += 1
                        break
                    else:
                        contents += 1
                        self.stdout += ", "
                        self.index += 2

                if self.tokens[self.index].key == TokenKeys.conjunto:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, self.tokens[self.index + 3].key, False, self.tokens[self.index + 5].key)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index += 4

                else:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += f"{self.getAssigDType(self.tokens[self.index].key, 0, False, None)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += "\t"
                self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, 0, False, None)}\n"

            self.index += 2

        self.genProcedimentoBlock()

    def genInicio(self) -> None:
        self.stdout += "\n# início\n"
        self.index += 1
        while True:
            token = self.tokens[self.index]

            match token.type:
                case TokenTypes.fim:
                    self.stdout += "# fim\n"
                    break
                case TokenTypes.leia:
                    self.genLeia()
                case TokenTypes.escreva:
                    self.genEscreva()
                case TokenTypes.id:
                    self.genId()
                case TokenTypes.se:
                    self.genSe()
                case TokenTypes.para:
                    self.genPara()
                case TokenTypes.enquanto:
                    self.genEnquanto()
                case _:
                    Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genProcedimentoBlock(self) -> None:
        self.index += 1
        while True:
            token = self.tokens[self.index]

            for i in range(self.level):
                self.stdout += "\t"

            match token.type:
                case TokenTypes.fim:
                    break
                case TokenTypes.leia:
                    self.genLeia()
                case TokenTypes.escreva:
                    self.genEscreva()
                case TokenTypes.id:
                    self.genId()
                case TokenTypes.se:
                    self.genSe()
                case TokenTypes.para:
                    self.genPara()
                case TokenTypes.enquanto:
                    self.genEnquanto()
                case _:
                    Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genBlock(self) -> None:
        self.stdout += "\n"
        while True:
            token = self.tokens[self.index]

            for i in range(self.level):
                self.stdout += "\t"

            match token.type:
                case TokenTypes.fimse | TokenTypes.senao | TokenTypes.fimpara | TokenTypes.fimenq:
                    self.stdout = self.stdout[:-1]
                    break
                case TokenTypes.leia:
                    self.genLeia()
                case TokenTypes.escreva:
                    self.genEscreva()
                case TokenTypes.id:
                    self.genId()
                case TokenTypes.se:
                    self.genSe()
                case TokenTypes.para:
                    self.genPara()
                case TokenTypes.enquanto:
                    self.genEnquanto()
                case _:
                    Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genSe(self) -> None:
        self.stdout += "if ("
        self.index += 2
        self.stdout += self.tokens[self.index].key

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += "["
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += "]"

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f"[{self.tokens[self.index].key}]"
                self.index += 1

            self.index += 1

        self.genExp()
        self.index += 1
        self.stdout += ":"
        self.level += 1

        while self.tokens[self.index].type != TokenTypes.fimse:
            self.genBlock()
            if self.tokens[self.index].type == TokenTypes.senao:
                self.stdout += "else:"
                self.index += 1
                self.genBlock()

        self.stdout += "\n"
        self.level -= 1
        self.index += 1

    def genPara(self) -> None:
        self.stdout += "for "
        self.index += 1
        self.stdout += self.tokens[self.index].key
        self.index += 1
        self.stdout += " in "

        if self.tokens[self.index].type == TokenTypes.numb:
            range_start = self.tokens[self.index].key
            self.index += 2
            range_end = self.tokens[self.index].key
            self.index += 2
            range_step = self.tokens[self.index].key
            self.stdout += f"range({range_start}, {range_end}, {range_step}):"
            self.index += 2

        elif self.tokens[self.index].type == TokenTypes.id:
            range_start = self.tokens[self.index].key
            self.index += 1
            aux_stdout = self.stdout
            self.stdout = ""
            self.genExp()
            exp = self.stdout
            range_start += exp
            self.stdout = aux_stdout
            self.index += 1
            range_end = self.tokens[self.index].key
            self.index += 2
            range_step = self.tokens[self.index].key
            self.stdout += f"range({range_start}, {range_end}, {range_step}):"
            self.index += 2

        self.level += 1

        if self.tokens[self.index].type != TokenTypes.fimpara:
            self.genBlock()

        self.level -= 1
        self.index += 1
        if not self.level:
            self.stdout += "\n"

    def genEnquanto(self) -> None:
        self.stdout += "while ("
        self.index += 2
        self.stdout += self.tokens[self.index].key
        self.index += 1

        self.genExp()
        self.stdout += ":"
        self.index += 1

        self.level += 1
        if self.tokens[self.index].type != TokenTypes.fimpara:
            self.genBlock()

        self.level -= 1
        self.index += 1
        self.stdout += "\n"

    def genVarAssign(self) -> None:
        self.index += 1
        self.stdout += " = "

        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += "("
            self.index += 1

        while self.tokens[self.index].type == TokenTypes.rParen:
            self.stdout += ")"
            self.index += 1

        self.stdout += self.tokens[self.index].key

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += "["
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += "]"

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f"[{self.tokens[self.index].key}]"
                self.index += 1

            self.index += 1

        if (
            self.tokens[self.index].type == TokenTypes.mathOps
            or self.tokens[self.index].type == TokenTypes.lParen
            or self.tokens[self.index].type == TokenTypes.rParen
        ):
            self.genExp()

        self.stdout += "\n"

    def genId(self) -> None:
        dtype = self.symtab.getType(self.tokens[self.index].key)
        if dtype == TokenTypes.procedimento or dtype == TokenTypes.funcao:
            self.stdout += f"{self.tokens[self.index].key}("

            self.index += 1
            if self.tokens[self.index].type == TokenTypes.lParen:

                self.index += 1
                while self.tokens[self.index].type != TokenTypes.rParen:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1
                    if self.tokens[self.index].type == TokenTypes.comma:
                        self.stdout += ", "
                        self.index += 1
                self.index += 1
            self.stdout += ")\n"

        else:
            self.stdout += self.tokens[self.index].key
            self.index += 1

        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += "["
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += "]"

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f"[{self.tokens[self.index].key}]"
                self.index += 1

            self.index += 1

        if self.tokens[self.index].type == TokenTypes.rArrow:
            self.genVarAssign()

    def genExp(self) -> None:
        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += "("
            self.index += 1

        if self.tokens[self.index].type == TokenTypes.logicalOps:
            while self.tokens[self.index].type == TokenTypes.logicalOps:
                self.stdout += f" {self.getLogical(self.tokens[self.index].key)} "

                self.index += 1
                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += "("
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ")"
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.str:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1

                elif self.tokens[self.index].type == TokenTypes.numb:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1

                elif self.tokens[self.index].type == TokenTypes.id:
                    self.stdout += self.tokens[self.index].key

                    self.index += 1
                    if self.tokens[self.index].type == TokenTypes.lSquare:
                        self.stdout += "["
                        self.index += 1
                        self.stdout += f"{self.tokens[self.index].key}"
                        self.index += 1
                        self.stdout += "]"

                        if self.tokens[self.index].type == TokenTypes.comma:
                            self.index += 1
                            self.stdout += f"[{self.tokens[self.index].key}]"
                            self.index += 1

                        self.index += 1

                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += "("
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ")"
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.mathOps:
                    self.genExp()

        elif self.tokens[self.index].type == TokenTypes.mathOps:
            while self.tokens[self.index].type == TokenTypes.mathOps:
                self.stdout += f" {self.getMath(self.tokens[self.index].key)} "

                self.index += 1
                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += "("
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ")"
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.str:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1

                elif self.tokens[self.index].type == TokenTypes.numb:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1

                elif self.tokens[self.index].type == TokenTypes.id:
                    self.stdout += self.tokens[self.index].key
                    self.index += 1

                    if self.tokens[self.index].type == TokenTypes.lSquare:
                        self.stdout += "["
                        self.index += 1
                        self.stdout += f"{self.tokens[self.index].key}"
                        self.index += 1
                        self.stdout += "]"

                        if self.tokens[self.index].type == TokenTypes.comma:
                            self.index += 1
                            self.stdout += f"[{self.tokens[self.index].key}]"
                            self.index += 1

                        self.index += 1

                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += "("
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ")"
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.logicalOps:
                    self.genExp()

        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += "("
            self.index += 1

        while self.tokens[self.index].type == TokenTypes.rParen:
            self.stdout += ")"
            self.index += 1

    def genLeia(self) -> None:
        self.index += 1

        input_var = self.tokens[self.index].key
        input_cast = self.getInputCast(self.tokens[self.index].key)

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.comma:
            self.stdout += f"{input_var} = {input_cast}\n"

            while self.tokens[self.index].type == TokenTypes.comma:
                self.stdout += f"{self.tokens[self.index + 1].key} = {self.getInputCast(self.tokens[self.index + 1].key)}\n"
                self.index += 2

        elif self.tokens[self.index].type == TokenTypes.lSquare:
            self.index += 1
            input_var_array_index = self.tokens[self.index].key
            self.index += 1
            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f"{input_var}[{input_var_array_index}][{self.tokens[self.index].key}] = {input_cast}\n"
                self.index += 2
            else:
                self.stdout += f"{input_var}[{input_var_array_index}] = {input_cast}\n"
                self.index += 1
        else:
            self.stdout += f"{input_var} = {input_cast}\n"

    def genEscreva(self) -> None:
        self.index += 1
        self.stdout += f"print({self.tokens[self.index].key}"
        self.index += 1

        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += "["
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += "]"

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f"[{self.tokens[self.index].key}]"
                self.index += 1

            self.index += 1

        while self.tokens[self.index].type == TokenTypes.mathOps:
            self.index += 1
            self.stdout += f", {self.tokens[self.index].key}"
            self.index += 1

        if self.tokens[self.index].type == TokenTypes.comma:
            while self.tokens[self.index].type == TokenTypes.comma:
                self.stdout += f", {self.tokens[self.index + 1].key}"
                self.index += 2
        self.stdout += ")\n"
