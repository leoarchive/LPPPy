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
from .error import Error, ErrorTypes
from .token import TokenKeys, TokenTypes

# Não há necessidade de armazenar tokens que não serão necessários para
# a geracão do código final, tal qual 'programa', 'var', ':', '[', ...
#
# Caso no decorrer do desenvolvimento haja necessidade, a geracão de código
# python deve ser inteiramente refatorada.
class Parser:
    token = None
    lexer = None
    symtab = None
    tokens = []
    ignore = [
        TokenTypes.programa,
        TokenTypes.var,
        TokenTypes.colon,
        TokenTypes.dPeriod,
        TokenTypes.de,
    ]

    def __init__(self, lexer, symtab):
        self.lexer = lexer
        self.symtab = symtab

    def run(self):
        self.parse()

    def eatToken(self, token, expectedType):
        if not token or token.type != expectedType:
            raise Error(ErrorTypes.parser_unexpected_token, token)

        if not token.type in self.ignore:
            self.tokens.append(token)

    def parse(self):
        self.eatToken(self.lexer.lex(), TokenTypes.programa)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        self.eatToken(self.lexer.lex(), TokenTypes.var)
        self.parseVarBlock(self.lexer.lex())

    def parseVarBlock(self, token):
        if token.type == TokenTypes.inicio:
            self.eatToken(token, TokenTypes.inicio)
            return self.parseInicio()

        if token.type == TokenTypes.procedimento:
            self.eatToken(token, TokenTypes.procedimento)
            token = self.lexer.lex()
            self.symtab.push(token, TokenTypes.call)
            self.eatToken(token, TokenTypes.id)
            self.eatToken(self.lexer.lex(), TokenTypes.var)
            token = self.parseProcedimento(self.lexer.lex())
            self.eatToken(token, TokenTypes.fim)
            return self.parseVarBlock(self.lexer.lex())
             
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

        self.parseVarBlock(self.lexer.lex())

    def parseProcedimento(self, token):
        if token.type == TokenTypes.inicio:
            self.eatToken(token, TokenTypes.inicio)
            return self.parseProcedimentoBlock()
    
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

    def parseInicio(self):
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

    def parseProcedimentoBlock(self):
        token = self.lexer.lex()
        while True:
            if token.type == TokenTypes.fim:
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

    def parseSeBlock(self):
        token = self.lexer.lex()
        while True:
            if token.type == TokenTypes.fimse or token.type == TokenTypes.senao:
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

    def parseEnquantoBlock(self):
        token = self.lexer.lex()
        while True:
            if token.type == TokenTypes.fim_enquanto:
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

    def parseParaBlock(self):
        token = self.lexer.lex()
        while True:
            if token.type == TokenTypes.fimpara:
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

    def parseSe(self, token):
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
            token = self.parseSeBlock()
            if token.type == TokenTypes.senao:
                self.eatToken(token, TokenTypes.senao)

        self.eatToken(token, TokenTypes.fimse)
        return self.lexer.lex()

    def parseEnquanto(self, token):
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
  
        if token.type != TokenTypes.fim_enquanto:
            token = self.parseEnquantoBlock()

        self.eatToken(token, TokenTypes.fim_enquanto)
        return self.lexer.lex()

    def parsePara(self, token):
        self.eatToken(token, TokenTypes.para)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        self.eatToken(self.lexer.lex(), TokenTypes.de)

        token = self.lexer.lex()
        if token.type == TokenTypes.numb:
            self.eatToken(token, TokenTypes.numb)
        else:
            self.eatToken(token, TokenTypes.id)

        token = self.lexer.lex()
        if token.type == TokenTypes.mathOps or token.type == TokenTypes.lParen or token.type == TokenTypes.rParen:
            token = self.parseExp(token)

        self.eatToken(token, TokenTypes.ate)
        self.eatToken(self.lexer.lex(), TokenTypes.numb)
        self.eatToken(self.lexer.lex(), TokenTypes.passo)
        self.eatToken(self.lexer.lex(), TokenTypes.numb)

        token = self.lexer.lex()
        self.eatToken(token, TokenTypes.faca)

        while token.type != TokenTypes.fimpara:
            token = self.parseParaBlock()

        self.eatToken(token, TokenTypes.fimpara)
        return self.lexer.lex()

    def parseId(self, token):
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
            
        return token

    def parseVarAssign(self, token):
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

  
        if token.type == TokenTypes.mathOps or token.type == TokenTypes.lParen or token.type == TokenTypes.rParen:
            token = self.parseExp(token)

        return token

    def parseExp(self, token):
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

        while token.type == TokenTypes.rParen:
            self.eatToken(token, TokenTypes.rParen)
            token = self.lexer.lex()

        return token

    def parseLeia(self, token):
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
            self.eatToken(self.lexer.lex(), TokenTypes.id)
            self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
            token = self.lexer.lex()

        return token

    def parseEscreva(self, token):
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
                else:
                    self.eatToken(token, TokenTypes.id)

                self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
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
