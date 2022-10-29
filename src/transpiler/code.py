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
from .token import TokenKeys, TokenTypes
from .error import Error, ErrorTypes

# Alguns tokens não são armazenados no array final de tokens (self.tokens),
# no parser os tokens que são ignorados estão presentes no array 'ignore'.
#
# Saber os tokens que são ignorados é necessários para iterar o array 'tokens'
# e dar saida (stdout) ao seu respectivo código em linguagem python.
class CodeGen:
    symtab = None
    tokens = []
    index = 0
    stdout = ""
    level = 0

    def __init__(self, symtab):
        self.symtab = symtab

    def run(self, tokens):
        self.tokens = tokens
 
        self.gen()

    def getDType(self, key):
        if key == TokenKeys.caractere:
            return "str"
        elif key == TokenKeys.inteiro:
            return "int"
        elif key == TokenKeys.real:
            return "float"
        else:
            return "None"

    def getAssigDType(self, key, size, matrix, _keytype):
        if key == TokenKeys.caractere:
            return "''"
        elif key == TokenKeys.inteiro:
            return "0"
        elif key == TokenKeys.real:
            return "0.0"
        elif key == TokenKeys.conjunto:
            if _keytype == TokenKeys.caractere:
                if matrix: return f"[['' for _ in range({size})] for _ in range({size})]"
                elif size: return f"[''] * {size}"
                else: return "['']"
            elif _keytype == TokenKeys.inteiro:
                if matrix and size: return f"[[0 for _ in range({size})] for _ in range({size})]"
                elif size: return f"[0] * {size}"
                else: return "[0]"
            elif _keytype == TokenKeys.real:
                if matrix: return f"[[0.0 for _ in range({size})] for _ in range({size})]"
                elif size: return f"[0.0] * {size}"
                else: return "[0.0]"
            else:
                if matrix: return f"[0][0]"
                elif size: return f"[] * {size}"
                else: return "[]"

    def getInputCast(self, key):
        type = self.symtab.getType(key)
        if type == TokenKeys.inteiro:
            return "int(input())"
        elif type == TokenKeys.real:
            return "float(input())"
        else:
            return "input()"

    def getLogical(self, key):
        if key == TokenKeys._and:
            return "and"
        elif key == TokenKeys._not:
            return "not"
        elif key == TokenKeys._or:
            return "or"
        elif key == TokenKeys.NotEq:
            return "!="
        elif key == TokenKeys.equal:
            return "=="
        else:
            return key

    def getMath(self, key):
        if key == TokenKeys.exponent:
            return "**"
        else:
            return key

    def gen(self):
        self.stdout = f"# programa {self.tokens[self.index].key}\n"
        self.index += 1

        while self.tokens[self.index].key == TokenKeys.procedimento:
            self.stdout += "\ndef "
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}():\n"
            self.index += 1
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
            self.index += 1
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
        self.genVarBlock()

    def genVarBlock(self):
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
                        self.stdout += (
                            f"{self.getAssigDType(self.tokens[self.index].key, 0, False, None)}"
                        )
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, 0, False, None)}\n"

            self.index += 2

        self.genInicio()

    def genProcedimento(self):
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
                        self.stdout += (
                            f"{self.getAssigDType(self.tokens[self.index].key, 0, False, None)}"
                        )
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += "\t"
                self.stdout += f"{self.tokens[self.index].key} = {self.getAssigDType(self.tokens[self.index + 1].key, 0, False, None)}\n"

            self.index += 2

        self.genProcedimentoBlock()

    def genInicio(self):
        self.stdout += "\n# início\n"
        self.index += 1
        while True:
            token = self.tokens[self.index]
            if token.type == TokenTypes.fim:
                self.stdout += "# fim\n"
                break
            elif token.type == TokenTypes.leia:
                self.genLeia()
            elif token.type == TokenTypes.escreva:
                self.genEscreva()
            elif token.type == TokenTypes.id:
                self.genId()
            elif token.type == TokenTypes.se:
                self.genSe()
            elif token.type == TokenTypes.para:
                self.genPara()
            elif token.type == TokenTypes.enquanto:
                self.genEnquanto()
            else:
                raise Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genProcedimentoBlock(self):
        self.index += 1
        while True:
            token = self.tokens[self.index]

            for i in range(self.level):
                self.stdout += "\t"

            if token.type == TokenTypes.fim:
                break
            elif token.type == TokenTypes.leia:
                self.genLeia()
            elif token.type == TokenTypes.escreva:
                self.genEscreva()
            elif token.type == TokenTypes.id:
                self.genId()
            elif token.type == TokenTypes.se:
                self.genSe()
            elif token.type == TokenTypes.para:
                self.genPara()
            elif token.type == TokenTypes.enquanto:
                self.genEnquanto()
            else:
                raise Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genSeBLock(self):
        self.stdout += "\n"
        while True:
            token = self.tokens[self.index]
          
            for i in range(self.level):
                self.stdout += "\t"

            if token.type == TokenTypes.fimse or token.type == TokenTypes.senao:
                self.stdout = self.stdout[:-1]
                break
            elif token.type == TokenTypes.leia:
                self.genLeia()
            elif token.type == TokenTypes.escreva:
                self.genEscreva()
            elif token.type == TokenTypes.id:
                self.genId()
            elif token.type == TokenTypes.se:
                self.genSe()
            elif token.type == TokenTypes.para:
                self.genPara()
            elif token.type == TokenTypes.enquanto:
                self.genEnquanto()
            else:
                raise Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genSe(self):
        self.stdout += "if ("
        self.index += 2
        self.stdout += self.tokens[self.index].key

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += '['
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += ']'

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f'[{self.tokens[self.index].key}]'
                self.index += 1

            self.index += 1

        self.genExp()
        self.index += 1
        self.stdout += ":"
        self.level += 1

        while self.tokens[self.index].type != TokenTypes.fimse:
            self.genSeBLock()
            if self.tokens[self.index].type == TokenTypes.senao:
                self.stdout += "else:"
                self.index += 1
                self.genSeBLock()
                
        self.stdout += "\n"
        self.level -= 1
        self.index += 1

    def genParaBLock(self):
        self.stdout += "\n"
        while True:
            token = self.tokens[self.index]
            
            for i in range(self.level):
                self.stdout += "\t"

            if token.type == TokenTypes.fimpara:
                self.stdout = self.stdout[:-1]
                break
            elif token.type == TokenTypes.leia:
                self.genLeia()
            elif token.type == TokenTypes.escreva:
                self.genEscreva()
            elif token.type == TokenTypes.id:
                self.genId()
            elif token.type == TokenTypes.se:
                self.genSe()
            elif token.type == TokenTypes.para:
                self.genPara()
            elif token.type == TokenTypes.enquanto:
                self.genEnquanto()
            else:
                raise Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genEnquantoBLock(self):
        self.stdout += "\n"
        while True:
            token = self.tokens[self.index]

            for i in range(self.level):
                self.stdout += "\t"

            if token.type == TokenTypes.fim_enquanto:
                self.stdout = self.stdout[:-1]
                break
            elif token.type == TokenTypes.leia:
                self.genLeia()
            elif token.type == TokenTypes.escreva:
                self.genEscreva()
            elif token.type == TokenTypes.id:
                self.genId()
            elif token.type == TokenTypes.se:
                self.genSe()
            elif token.type == TokenTypes.para:
                self.genPara()
            elif token.type == TokenTypes.enquanto:
                self.genEnquanto()
            else:
                raise Error(ErrorTypes.code_internal_error_not_implemented_yet, token)

    def genPara(self):
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
            self.stdout = ''
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
            self.genParaBLock()

        self.level -= 1
        self.index += 1
        if not self.level:
            self.stdout += "\n"

    def genEnquanto(self):
        self.stdout += "while ("
        self.index += 2
        self.stdout += self.tokens[self.index].key
        self.index += 1

        self.genExp()
        self.stdout += ":"
        self.index += 1

        self.level += 1
        if self.tokens[self.index].type != TokenTypes.fimpara:
            self.genEnquantoBLock()

        self.level -= 1
        self.index += 1
        if not self.level:
            self.stdout += "\n"

    def genVarAssign(self):
        self.index += 1
        self.stdout += " = "

        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += '('
            self.index += 1

        while self.tokens[self.index].type == TokenTypes.rParen:
            self.stdout += ')'
            self.index += 1

        self.stdout += self.tokens[self.index].key

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += '['
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += ']'

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f'[{self.tokens[self.index].key}]'
                self.index += 1

            self.index += 1
            
        if self.tokens[self.index].type == TokenTypes.mathOps or self.tokens[self.index].type == TokenTypes.lParen or self.tokens[self.index].type == TokenTypes.rParen:
            self.genExp()

        self.stdout += "\n"

    def genId(self):
        dtype = self.symtab.getType(self.tokens[self.index].key)
        if dtype == TokenTypes.procedimento:
            self.stdout += f"{self.tokens[self.index].key}()\n"

        else: 
            self.stdout += self.tokens[self.index].key

        self.index += 1

        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += '['
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += ']'

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f'[{self.tokens[self.index].key}]'
                self.index += 1

            self.index += 1

        if self.tokens[self.index].type == TokenTypes.rArrow:
            self.genVarAssign()

    def genExp(self):
        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += '('
            self.index += 1

        if self.tokens[self.index].type == TokenTypes.logicalOps:
            while self.tokens[self.index].type == TokenTypes.logicalOps:
                self.stdout += f" {self.getLogical(self.tokens[self.index].key)} "

                self.index += 1
                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += '('
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ')'
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
                        self.stdout += '['
                        self.index += 1
                        self.stdout += f"{self.tokens[self.index].key}"
                        self.index += 1
                        self.stdout += ']'

                        if self.tokens[self.index].type == TokenTypes.comma:
                            self.index += 1
                            self.stdout += f'[{self.tokens[self.index].key}]'
                            self.index += 1

                        self.index += 1

                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += '('
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ')'
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.mathOps:
                    self.genExp()

        elif self.tokens[self.index].type == TokenTypes.mathOps:
            while self.tokens[self.index].type == TokenTypes.mathOps:
                self.stdout += f" {self.getMath(self.tokens[self.index].key)} "

                self.index += 1
                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += '('
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ')'
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
                        self.stdout += '['
                        self.index += 1
                        self.stdout += f"{self.tokens[self.index].key}"
                        self.index += 1
                        self.stdout += ']'

                        if self.tokens[self.index].type == TokenTypes.comma:
                            self.index += 1
                            self.stdout += f'[{self.tokens[self.index].key}]'
                            self.index += 1

                        self.index += 1

                while self.tokens[self.index].type == TokenTypes.lParen:
                    self.stdout += '('
                    self.index += 1

                while self.tokens[self.index].type == TokenTypes.rParen:
                    self.stdout += ')'
                    self.index += 1

                if self.tokens[self.index].type == TokenTypes.logicalOps:
                    self.genExp()

        while self.tokens[self.index].type == TokenTypes.lParen:
            self.stdout += '('
            self.index += 1

        while self.tokens[self.index].type == TokenTypes.rParen:
            self.stdout += ')'
            self.index += 1

    def genLeia(self):
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
 
        # self.stdout += "\n"

    def genEscreva(self):
        self.index += 1
        self.stdout += f"print({self.tokens[self.index].key}"
        self.index += 1

        if self.tokens[self.index].type == TokenTypes.lSquare:
            self.stdout += '['
            self.index += 1
            self.stdout += f"{self.tokens[self.index].key}"
            self.index += 1
            self.stdout += ']'

            if self.tokens[self.index].type == TokenTypes.comma:
                self.index += 1
                self.stdout += f'[{self.tokens[self.index].key}]'
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
