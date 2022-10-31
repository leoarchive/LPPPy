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
from compiler.lex import Lexer
from compiler.symtab import Symtab
from .error import Error, ErrorTypes
from .token import Token, TokenKeys, TokenTypes


class Parser:
    lexer: Lexer = None
    symtab: Symtab = None
    tokens: list[Token] = []
    ignore: list[TokenTypes] = [
        TokenTypes.programa,
        TokenTypes.colon,
        TokenTypes.dPeriod,
        TokenTypes.de,
    ]

    def __init__(self, lexer: Lexer, symtab: Symtab) -> None:
        self.lexer = lexer
        self.symtab = symtab

    def run(self) -> None:
        self.parse()

    def eatToken(self, token: Token, expectedType: TokenTypes) -> None:
        if not token or token.type != expectedType:
            raise Error(ErrorTypes.parser_unexpected_token, token)

        if not token.type in self.ignore:
            self.tokens.append(token)

    def parse(self) -> None:
        self.eatToken(self.lexer.lex(), TokenTypes.programa)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        token = self.lexer.lex()

        while token.type == TokenTypes.procedimento:
            self.eatToken(token, TokenTypes.procedimento)
            token = self.lexer.lex()
            self.symtab.push(token, TokenTypes.procedimento)
            self.eatToken(token, TokenTypes.id)
            token = self.lexer.lex()

            if token.type == TokenTypes.var:
                self.eatToken(token, TokenTypes.var)
                token = self.lexer.lex()

            token = self.parseProcedimento(token)
            self.eatToken(token, TokenTypes.fim)
            token = self.lexer.lex()

        while token.type == TokenTypes.funcao:
            self.eatToken(token, TokenTypes.funcao)
            token = self.lexer.lex()
            self.symtab.push(token, TokenTypes.funcao)
            self.eatToken(token, TokenTypes.id)
            self.eatToken(self.lexer.lex(), TokenTypes.lParen)

            token = self.lexer.lex()
            while token.type != TokenTypes.rParen:
                self.eatToken(token, TokenTypes.id)
                token = self.lexer.lex()

                if token.type == TokenTypes.colon:
                    self.eatToken(token, TokenTypes.colon)
                    self.eatToken(self.lexer.lex(), TokenTypes.dType)

                if token.type == TokenTypes.comma:
                    self.eatToken(token, TokenTypes.comma)

                token = self.lexer.lex()

            self.eatToken(token, TokenTypes.rParen)

            token = self.lexer.lex()
            if token.type == TokenTypes.colon:
                self.eatToken(token, TokenTypes.colon)
                self.eatToken(self.lexer.lex(), TokenTypes.dType)
                token = self.lexer.lex()

            if token.type == TokenTypes.var:
                self.eatToken(token, TokenTypes.var)
                token = self.lexer.lex()

            token = self.parseProcedimento(token)
            self.eatToken(token, TokenTypes.fim)
            token = self.lexer.lex()

        if token.type == TokenTypes.tipo:
            self.eatToken(token, TokenTypes.tipo)
            token = self.lexer.lex()
            while token.type != TokenTypes.var:
                self.symtab.pushDType(token)
                self.eatToken(token, TokenTypes.id)
                token = self.lexer.lex()
                if token.key == TokenKeys.equal:
                    self.eatToken(token, TokenTypes.logicalOps)
                    self.eatToken(self.lexer.lex(), TokenTypes.registro)
                    self.parseRegistro(self.lexer.lex())
                token = self.lexer.lex()

        self.eatToken(token, TokenTypes.var)
        self.parseVar(self.lexer.lex())

    def parseVar(self, token: Token) -> None:
        if token.type == TokenTypes.inicio:
            self.eatToken(token, TokenTypes.inicio)
            return self.parseInicio()

        self.eatToken(token, TokenTypes.id)

        _symtokens = []
        _symtokens.append(token)

        token = self.lexer.lex()
        if token.type == TokenTypes.comma:
            while token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                token = self.lexer.lex()
                _symtokens.append(token)
                self.eatToken(token, TokenTypes.id)
                token = self.lexer.lex()

        self.eatToken(token, TokenTypes.colon)

        _symtype = 0

        token = self.lexer.lex()
        _symtype = token.key
        if token.type == TokenTypes.id:
            if self.symtab.checkDType(token.key):
                self.eatToken(token, TokenTypes.id)
            else:
                self.eatToken(token, TokenTypes.dType)
        else:
            self.eatToken(token, TokenTypes.dType)
        if token.key == TokenKeys.conjunto:
            self.eatToken(self.lexer.lex(), TokenTypes.lSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            token = self.lexer.lex()
            if token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                self.eatToken(self.lexer.lex(), TokenTypes.numb)
                self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
                self.eatToken(self.lexer.lex(), TokenTypes.numb)
                token = self.lexer.lex()
            self.eatToken(token, TokenTypes.rSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.de)
            token = self.lexer.lex()

            _symtype = token.key
            self.eatToken(token, TokenTypes.dType)

        for _token in _symtokens:
            self.symtab.push(_token, _symtype)

        self.parseVar(self.lexer.lex())

    def parseRegistro(self, token: Token) -> None:
        if token.type == TokenTypes.fimreg:
            return self.eatToken(token, TokenTypes.fimreg)

        self.eatToken(token, TokenTypes.id)

        _symtokens = []
        _symtokens.append(token)

        token = self.lexer.lex()
        if token.type == TokenTypes.comma:
            while token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                token = self.lexer.lex()
                _symtokens.append(token)
                self.eatToken(token, TokenTypes.id)
                token = self.lexer.lex()

        self.eatToken(token, TokenTypes.colon)

        _symtype = 0

        token = self.lexer.lex()
        _symtype = token.key
        self.eatToken(token, TokenTypes.dType)
        if token.key == TokenKeys.conjunto:
            self.eatToken(self.lexer.lex(), TokenTypes.lSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            token = self.lexer.lex()
            if token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                self.eatToken(self.lexer.lex(), TokenTypes.numb)
                self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
                self.eatToken(self.lexer.lex(), TokenTypes.numb)
                token = self.lexer.lex()
            self.eatToken(token, TokenTypes.rSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.de)
            token = self.lexer.lex()

            _symtype = token.key
            self.eatToken(token, TokenTypes.dType)

        for _token in _symtokens:
            self.symtab.push(_token, _symtype)

        self.parseRegistro(self.lexer.lex())

    def parseProcedimento(self, token: Token) -> None:
        if token.type == TokenTypes.inicio:
            self.eatToken(token, TokenTypes.inicio)
            return self.parseBlock()

        self.eatToken(token, TokenTypes.id)

        _symtokens = []
        _symtokens.append(token)

        token = self.lexer.lex()
        if token.type == TokenTypes.comma:
            while token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                token = self.lexer.lex()
                _symtokens.append(token)
                self.eatToken(token, TokenTypes.id)
                token = self.lexer.lex()

        self.eatToken(token, TokenTypes.colon)

        _symtype = 0

        token = self.lexer.lex()
        _symtype = token.key
        self.eatToken(token, TokenTypes.dType)
        if token.key == TokenKeys.conjunto:
            self.eatToken(self.lexer.lex(), TokenTypes.lSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
            self.eatToken(self.lexer.lex(), TokenTypes.numb)
            self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
            self.eatToken(self.lexer.lex(), TokenTypes.de)
            token = self.lexer.lex()

            _symtype = token.key
            self.eatToken(token, TokenTypes.dType)

        for _token in _symtokens:
            self.symtab.push(_token, _symtype)

        return self.parseProcedimento(self.lexer.lex())

    def parseInicio(self) -> None:
        token = self.lexer.lex()
        while True:
            if token.type == TokenTypes.fim:
                return self.eatToken(token, TokenTypes.fim)
            elif token.type == TokenTypes.id:
                token = self.parseId(token)
            elif token.type == TokenTypes.leia:
                token = self.parseLeia(token)
            elif token.type == TokenTypes.escreva:
                token = self.parseEscreva(token)
            elif token.type == TokenTypes.se:
                token = self.parseSe(token)
            elif token.type == TokenTypes.enquanto:
                token = self.parseEnquanto(token)
            elif token.type == TokenTypes.para:
                token = self.parsePara(token)
            else:
                raise Error(ErrorTypes.parser_unexpected_token, token)

    def parseBlock(self) -> None:
        token = self.lexer.lex()
        while True:
            if (
                token.type == TokenTypes.fimse
                or token.type == TokenTypes.senao
                or token.type == TokenTypes.fim
                or token.type == TokenTypes.fimenq
                or token.type == TokenTypes.fimpara
            ):
                return token
            elif token.type == TokenTypes.id:
                token = self.parseId(token)
            elif token.type == TokenTypes.leia:
                token = self.parseLeia(token)
            elif token.type == TokenTypes.escreva:
                token = self.parseEscreva(token)
            elif token.type == TokenTypes.se:
                token = self.parseSe(token)
            elif token.type == TokenTypes.para:
                token = self.parsePara(token)
            elif token.type == TokenTypes.enquanto:
                token = self.parseEnquanto(token)
            else:
                raise Error(ErrorTypes.parser_unexpected_token, token)

    def parseSe(self, token) -> None:
        self.eatToken(token, TokenTypes.se)
        self.eatToken(self.lexer.lex(), TokenTypes.lParen)

        token = self.lexer.lex()
        if token.type == TokenTypes.numb:
            self.eatToken(token, TokenTypes.numb)
            token = self.lexer.lex()
        elif token.type == TokenTypes.id:
            self.eatToken(token, TokenTypes.id)

            token = self.lexer.lex()
            if token.type == TokenTypes.lSquare:
                self.eatToken(token, TokenTypes.lSquare)

                token = self.lexer.lex()
                if token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                else:
                    self.eatToken(token, TokenTypes.id)

                self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
                token = self.lexer.lex()

        elif token.type == TokenTypes.str:
            self.eatToken(token, TokenTypes.str)
            token = self.lexer.lex()

        token = self.parseExp(token)

        self.eatToken(token, TokenTypes.entao)

        while token.type != TokenTypes.fimse:
            token = self.parseBlock()
            if token.type == TokenTypes.senao:
                self.eatToken(token, TokenTypes.senao)

        self.eatToken(token, TokenTypes.fimse)
        return self.lexer.lex()

    def parseEnquanto(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.enquanto)
        self.eatToken(self.lexer.lex(), TokenTypes.lParen)

        token = self.lexer.lex()
        if token.type == TokenTypes.numb:
            self.eatToken(token, TokenTypes.numb)
            token = self.lexer.lex()
        elif token.type == TokenTypes.id:
            self.eatToken(token, TokenTypes.id)

            token = self.lexer.lex()
            if token.type == TokenTypes.lSquare:
                self.eatToken(token, TokenTypes.lSquare)

                token = self.lexer.lex()
                if token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                else:
                    self.eatToken(token, TokenTypes.id)

                self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
                token = self.lexer.lex()

        elif token.type == TokenTypes.str:
            self.eatToken(token, TokenTypes.str)
            token = self.lexer.lex()

        token = self.parseExp(token)

        self.eatToken(token, TokenTypes.faca)

        if token.type != TokenTypes.fimenq:
            token = self.parseBlock()

        self.eatToken(token, TokenTypes.fimenq)
        return self.lexer.lex()

    def parsePara(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.para)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        self.eatToken(self.lexer.lex(), TokenTypes.de)

        token = self.lexer.lex()
        if token.type == TokenTypes.numb:
            self.eatToken(token, TokenTypes.numb)
        else:
            self.eatToken(token, TokenTypes.id)

        token = self.lexer.lex()
        if (
            token.type == TokenTypes.mathOps
            or token.type == TokenTypes.lParen
            or token.type == TokenTypes.rParen
        ):
            token = self.parseExp(token)

        self.eatToken(token, TokenTypes.ate)
        self.eatToken(self.lexer.lex(), TokenTypes.numb)
        self.eatToken(self.lexer.lex(), TokenTypes.passo)
        self.eatToken(self.lexer.lex(), TokenTypes.numb)

        token = self.lexer.lex()
        self.eatToken(token, TokenTypes.faca)

        while token.type != TokenTypes.fimpara:
            token = self.parseBlock()

        self.eatToken(token, TokenTypes.fimpara)
        return self.lexer.lex()

    def parseId(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.id)

        token = self.lexer.lex()
        if token.type == TokenTypes.lSquare:
            self.eatToken(token, TokenTypes.lSquare)

            token = self.lexer.lex()
            if token.type == TokenTypes.numb:
                self.eatToken(token, TokenTypes.numb)
            else:
                self.eatToken(token, TokenTypes.id)

            self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
            token = self.lexer.lex()

        if token.type == TokenTypes.rArrow:
            token = self.parseVarAssign(token)
        elif token.type == TokenTypes.lParen:
            self.eatToken(token, TokenTypes.lParen)
            token = self.lexer.lex()

            while token.type != TokenTypes.rParen:
                if token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                    token = self.lexer.lex()

                elif token.type == TokenTypes.id:
                    self.eatToken(token, TokenTypes.id)
                    token = self.lexer.lex()

                    if token.type == TokenTypes.lSquare:
                        self.eatToken(token, TokenTypes.lSquare)

                        token = self.lexer.lex()
                        if token.type == TokenTypes.numb:
                            self.eatToken(token, TokenTypes.numb)
                        else:
                            self.eatToken(token, TokenTypes.id)

                        self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
                        token = self.lexer.lex()
                    elif token.type == TokenTypes.comma:
                        self.eatToken(token, TokenTypes.comma)
                        token = self.lexer.lex()

                elif token.type == TokenTypes.str:
                    self.eatToken(token, TokenTypes.str)
                    token = self.lexer.lex()

            self.eatToken(token, TokenTypes.rParen)
            token = self.lexer.lex()

        return token

    def parseVarAssign(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.rArrow)

        token = self.lexer.lex()
        while token.type == TokenTypes.lParen:
            self.eatToken(token, TokenTypes.lParen)
            token = self.lexer.lex()

        while token.type == TokenTypes.rParen:
            self.eatToken(token, TokenTypes.rParen)
            token = self.lexer.lex()

        if token.type == TokenTypes.numb:
            self.eatToken(token, TokenTypes.numb)
        elif token.type == TokenTypes.id:
            self.eatToken(token, TokenTypes.id)
        elif token.type == TokenTypes.str:
            self.eatToken(token, TokenTypes.str)

        token = self.lexer.lex()
        while token.type == TokenTypes.lParen:
            self.eatToken(token, TokenTypes.lParen)
            token = self.lexer.lex()

        while token.type == TokenTypes.rParen:
            self.eatToken(token, TokenTypes.rParen)
            token = self.lexer.lex()

        if token.type == TokenTypes.lSquare:
            self.eatToken(token, TokenTypes.lSquare)

            token = self.lexer.lex()
            if token.type == TokenTypes.numb:
                self.eatToken(token, TokenTypes.numb)
            elif token.type == TokenTypes.id:
                self.eatToken(token, TokenTypes.id)

            self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
            token = self.lexer.lex()

        if (
            token.type == TokenTypes.mathOps
            or token.type == TokenTypes.lParen
            or token.type == TokenTypes.rParen
        ):
            token = self.parseExp(token)

        return token

    def parseExp(self, token: Token) -> None:
        while token.type == TokenTypes.lParen:
            self.eatToken(token, TokenTypes.lParen)
            token = self.lexer.lex()

        if token.type == TokenTypes.logicalOps:
            while token.type == TokenTypes.logicalOps:
                self.eatToken(token, TokenTypes.logicalOps)

                token = self.lexer.lex()
                while token.type == TokenTypes.lParen:
                    self.eatToken(token, TokenTypes.lParen)
                    token = self.lexer.lex()

                while token.type == TokenTypes.rParen:
                    self.eatToken(token, TokenTypes.rParen)
                    token = self.lexer.lex()

                if token.type == TokenTypes.str:
                    self.eatToken(token, TokenTypes.str)
                    token = self.lexer.lex()

                elif token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                    token = self.lexer.lex()

                elif token.type == TokenTypes.id:
                    self.eatToken(token, TokenTypes.id)
                    token = self.lexer.lex()

                    if token.type == TokenTypes.lSquare:
                        self.eatToken(token, TokenTypes.lSquare)

                        token = self.lexer.lex()
                        if token.type == TokenTypes.numb:
                            self.eatToken(token, TokenTypes.numb)
                        else:
                            self.eatToken(token, TokenTypes.id)

                        self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
                        token = self.lexer.lex()

                while token.type == TokenTypes.lParen:
                    self.eatToken(token, TokenTypes.lParen)
                    token = self.lexer.lex()

                while token.type == TokenTypes.rParen:
                    self.eatToken(token, TokenTypes.rParen)
                    token = self.lexer.lex()

                if token.type == TokenTypes.mathOps:
                    return self.parseExp(token)

        elif token.type == TokenTypes.mathOps:
            while token.type == TokenTypes.mathOps:
                self.eatToken(token, TokenTypes.mathOps)

                token = self.lexer.lex()
                while token.type == TokenTypes.lParen:
                    self.eatToken(token, TokenTypes.lParen)
                    token = self.lexer.lex()

                while token.type == TokenTypes.rParen:
                    self.eatToken(token, TokenTypes.rParen)
                    token = self.lexer.lex()

                if token.type == TokenTypes.str:
                    self.eatToken(token, TokenTypes.str)
                    token = self.lexer.lex()

                elif token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                    token = self.lexer.lex()

                elif token.type == TokenTypes.id:
                    self.eatToken(token, TokenTypes.id)
                    token = self.lexer.lex()

                    if token.type == TokenTypes.lSquare:
                        self.eatToken(token, TokenTypes.lSquare)

                        token = self.lexer.lex()
                        if token.type == TokenTypes.numb:
                            self.eatToken(token, TokenTypes.numb)
                        else:
                            self.eatToken(token, TokenTypes.id)

                        self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
                        token = self.lexer.lex()

                while token.type == TokenTypes.lParen:
                    self.eatToken(token, TokenTypes.lParen)
                    token = self.lexer.lex()

                while token.type == TokenTypes.rParen:
                    self.eatToken(token, TokenTypes.rParen)
                    token = self.lexer.lex()

                if token.type == TokenTypes.logicalOps:
                    return self.parseExp(token)

        while token.type == TokenTypes.rParen:
            self.eatToken(token, TokenTypes.rParen)
            token = self.lexer.lex()

        return token

    def parseLeia(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.leia)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        token = self.lexer.lex()
        if token.type == TokenTypes.comma:
            while token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                self.eatToken(self.lexer.lex(), TokenTypes.id)
                token = self.lexer.lex()
        elif token.type == TokenTypes.lSquare:
            self.eatToken(token, TokenTypes.lSquare)
            token = self.lexer.lex()
            if token.type == TokenTypes.id:
                self.eatToken(token, TokenTypes.id)
            else:
                self.eatToken(token, TokenTypes.numb)
            token = self.lexer.lex()
            if token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                token = self.lexer.lex()
                if token.type == TokenTypes.id:
                    self.eatToken(token, TokenTypes.id)
                else:
                    self.eatToken(token, TokenTypes.numb)
                token = self.lexer.lex()

            self.eatToken(token, TokenTypes.rSquare)
            token = self.lexer.lex()

        return token

    def parseEscreva(self, token: Token) -> None:
        self.eatToken(token, TokenTypes.escreva)

        token = self.lexer.lex()
        if token.type == TokenTypes.str:
            self.eatToken(token, TokenTypes.str)
            token = self.lexer.lex()

            if token.type == TokenTypes.mathOps:
                while token.type == TokenTypes.mathOps:
                    self.eatToken(token, TokenTypes.mathOps)
                    token = self.lexer.lex()
                    if token.type == TokenTypes.numb:
                        self.eatToken(token, TokenTypes.numb)
                    elif token.type == TokenTypes.str:
                        self.eatToken(token, TokenTypes.str)
                    else:
                        self.eatToken(token, TokenTypes.id)
                    token = self.lexer.lex()

        elif token.type == TokenTypes.id:
            self.eatToken(token, TokenTypes.id)

            token = self.lexer.lex()
            if token.type == TokenTypes.lSquare:
                self.eatToken(token, TokenTypes.lSquare)

                token = self.lexer.lex()
                if token.type == TokenTypes.numb:
                    self.eatToken(token, TokenTypes.numb)
                elif token.type == TokenTypes.str:
                    self.eatToken(token, TokenTypes.str)
                else:
                    self.eatToken(token, TokenTypes.id)

                token = self.lexer.lex()

                if token.type == TokenTypes.comma:
                    self.eatToken(token, TokenTypes.comma)
                    token = self.lexer.lex()
                    if token.type == TokenTypes.numb:
                        self.eatToken(token, TokenTypes.numb)
                    else:
                        self.eatToken(token, TokenTypes.id)
                    token = self.lexer.lex()

                self.eatToken(token, TokenTypes.rSquare)
                token = self.lexer.lex()

        if token.type == TokenTypes.comma:
            while token.type == TokenTypes.comma:
                self.eatToken(token, TokenTypes.comma)
                token = self.lexer.lex()
                if token.type == TokenTypes.str:
                    self.eatToken(token, TokenTypes.str)
                elif token.type == TokenTypes.id:
                    self.eatToken(token, TokenTypes.id)

                token = self.lexer.lex()

        return token
