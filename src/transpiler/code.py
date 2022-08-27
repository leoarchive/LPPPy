#
# This file is part of the LPPPy distribution (https://github.com/leozamboni/LPPPy).
# Copyright (c) 2022 IFRS - Campus Vacaria.
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

    def __init__(self, symtab):
        self.symtab = symtab

    def run(self, tokens):
        self.tokens = tokens

        self.gen()

    def getDType(self, key, _keytype):
        if key == TokenKeys.caractere:
            return "''"
        elif key == TokenKeys.inteiro:
            return "0"
        elif key == TokenKeys.real:
            return "0.0"
        elif key == TokenKeys.conjunto:
            if _keytype == TokenKeys.caractere:
                return "['']"
            elif _keytype == TokenKeys.inteiro:
                return "[0]"
            elif _keytype == TokenKeys.real:
                return "[0.0]"
            else:
                return "[]"

    def getInputCast(self, key):
        type = self.symtab.getType(key)
        if type == TokenKeys.caractere:
            return "input()"
        elif type == TokenKeys.inteiro:
            return "int(input())"
        elif type == TokenKeys.real:
            return "float(input())"

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

    def gen(self):
        self.stdout = f"# programa {self.tokens[self.index].key}\n"
        self.stdout += "# var\n"
        self.index += 1

        self.genVarBlock()

    def genVarBlock(self):
        while self.tokens[self.index].type != TokenTypes.inicio:
            if self.tokens[self.index + 1].key == TokenKeys.conjunto:
                self.stdout += f"{self.tokens[self.index].key} = {self.getDType(self.tokens[self.index + 1].key, self.tokens[self.index + 6].key)}\n"
                self.index += 5

            elif self.tokens[self.index + 1].key == TokenKeys.dot:
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
                        self.stdout += f"{self.getDType(self.tokens[self.index].key, self.tokens[self.index + 5].key)}"
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index += 4

                else:
                    self.stdout += " = "

                    for x in range(0, contents):
                        self.stdout += (
                            f"{self.getDType(self.tokens[self.index].key, None)}"
                        )
                        if x < contents - 1:
                            self.stdout += ", "

                    self.stdout += "\n"
                    self.index -= 1

            else:
                self.stdout += f"{self.tokens[self.index].key} = {self.getDType(self.tokens[self.index + 1].key, None)}\n"

            self.index += 2

        self.genInicio()

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
            else:
                print(f"NOT IMPLEMENTED YET: {token.type}\n")
                return 

    def genSeBLock(self):
        self.stdout += "\n"
        while True:
            token = self.tokens[self.index]
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
            else:
                print(f"NOT IMPLEMENTED YET: {token.type}\n")
                return

    def genSe(self):
        self.stdout += "if "
        self.index += 2
        self.stdout += self.tokens[self.index].key

        self.index += 1
        self.genExp()
        self.index += 1
        self.stdout += ":"

        self.index += 1
        while self.tokens[self.index].type != TokenTypes.fimse:
            self.genSeBLock()
            if self.tokens[self.index].type == TokenTypes.senao:
                self.stdout += "else:"
                self.index += 1
                self.genSeBLock()

        self.index += 1

    def genVarAssign(self):
        self.index += 1
        self.stdout += f" = {self.tokens[self.index].key}"

        self.index += 1
        if self.tokens[self.index].type == TokenTypes.mathOps:
            self.genExp()

        self.stdout += "\n"

    def genId(self):
        self.stdout += self.tokens[self.index].key
        self.index += 1
        if self.tokens[self.index].type == TokenTypes.rArrow:
            self.genVarAssign()

    def genExp(self):
        if self.tokens[self.index].type == TokenTypes.logicalOps:
            while self.tokens[self.index].type == TokenTypes.logicalOps:
                self.stdout += f" {self.getLogical(self.tokens[self.index].key)} "

                self.index += 1
                if self.tokens[self.index].type == TokenTypes.numb:
                    self.stdout += self.tokens[self.index].key
                elif self.tokens[self.index].type == TokenTypes.id:
                    self.stdout += self.tokens[self.index].key

                self.index += 1

        elif self.tokens[self.index].type == TokenTypes.mathOps:
            while self.tokens[self.index].type == TokenTypes.mathOps:
                self.stdout += f" {self.tokens[self.index].key} "

                self.index += 1
                if self.tokens[self.index].type == TokenTypes.numb:
                    self.stdout += self.tokens[self.index].key
                elif self.tokens[self.index].type == TokenTypes.id:
                    self.stdout += self.tokens[self.index].key

                self.index += 1

    def genLeia(self):
        self.index += 1
        self.stdout += f"{self.tokens[self.index].key} = {self.getInputCast(self.tokens[self.index].key)}\n"
        self.index += 1
        if self.tokens[self.index].type == TokenTypes.dot:
            while self.tokens[self.index].type == TokenTypes.dot:
                self.stdout += f"{self.tokens[self.index + 1].key} = {self.getInputCast(self.tokens[self.index + 1].key)}\n"
                self.index += 2

    def genEscreva(self):
        self.index += 1
        self.stdout += f"print({self.tokens[self.index].key}"
        self.index += 1
        if self.tokens[self.index].type == TokenTypes.dot:
            while self.tokens[self.index].type == TokenTypes.dot:
                self.stdout += f", {self.tokens[self.index + 1].key}"
                self.index += 2
        self.stdout += ")\n"
