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
from .token import Token, TokenTypes, TokenKeys


class Lexer:
    stdin = ""
    index = 0
    line = 1

    keyWords = [
        TokenKeys.programa,
        TokenKeys.var,
        TokenKeys.leia,
        TokenKeys.escreva,
        TokenKeys.caractere,
        TokenKeys.real,
        TokenKeys.inicio,
        TokenKeys.fim,
        TokenKeys.conjunto,
        TokenKeys.dPeriod,
        TokenKeys.de,
        TokenKeys.se,
        TokenKeys.inteiro,
        TokenKeys.entao,
        TokenKeys.graterEq,
        TokenKeys.lessEq,
        TokenKeys.NotEq,
        TokenKeys.fimse,
        TokenKeys.senao,
        TokenKeys._and,
        TokenKeys._not,
        TokenKeys._or,
        TokenKeys.grater,
        TokenKeys.less,
        TokenKeys.equal,
        TokenKeys.para,
        TokenKeys.fimpara,
        TokenKeys.ate,
        TokenKeys.passo,
        TokenKeys.faca,
        TokenKeys.mod,
        TokenKeys.enquanto,
        TokenKeys.fim_enquanto,
        TokenKeys.procedimento,
    ]
    keyChars = [
        TokenKeys.minus,
        TokenKeys.plus,
        TokenKeys.mult,
        TokenKeys.div,
        TokenKeys.rArrow,
        TokenKeys.lArrow,
        TokenKeys.rParen,
        TokenKeys.lParen,
        TokenKeys.colon,
        TokenKeys.rSquare,
        TokenKeys.comma,
        TokenKeys.lSquare,
        TokenKeys.exponent,
    ]
    chars = ["\n"]

    def __init__(self, stdin):
        self.stdin = stdin

    def lex_dotwords(self):
        start = self.index
        self.index += 1

        while self.stdin[self.index] != ".":
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        self.index += 1
        key = self.stdin[start : self.index]
        token = self.lex_keyword(key)
        if token:
            return token
        return Token(key, TokenTypes.id, self.line)

    def lex_string(self):
        start = self.index
        self.index += 1

        while self.stdin[self.index] != '"':
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        self.index += 1

        key = self.stdin[start : self.index]
        return Token(key, TokenTypes.str, self.line)

    def lex_alpha(self):
        start = self.index
        while (
            self.isAlphaOrOP(self.stdin[self.index])
            or self.stdin[self.index].isnumeric()
        ):
            self.index += 1
            if len(self.stdin) <= self.index:
                break

        key = self.stdin[start : self.index]
        token = self.lex_keyword(key)
        if token:
            return token
        return Token(key, TokenTypes.id, self.line)

    def lex_number(self):
        start = self.index
        while len(self.stdin) > self.index and (self.stdin[self.index].isnumeric() or (self.stdin[self.index] == '.' and self.stdin[self.index + 1].isnumeric())):
            self.index += 1

        key = self.stdin[start : self.index]
        return Token(key, TokenTypes.numb, self.line)

    def lex_keyword(self, key):
        for keyWord in self.keyWords:
            if key == keyWord:
                return Token(key, Token.getType(key), self.line)

    def lex_keychar(self, key):
        for keyChar in self.keyChars:
            if key == keyChar[0]:
                self.index += 1
                return Token(key, Token.getType(key), self.line)

    def lex_chars(self, key):
        for char in self.chars:
            if key == char:
                if key == "\n":
                    self.line += 1
                    break

    def isAlphaOrOP(self, key):
        return key.isalpha() or key == "=" or key == "<" or key == ">" or key == "_"

    def lex(self):
        if len(self.stdin) <= self.index:
            raise Error(
                ErrorTypes.lexer_unexpected_token, {"key": "eof", "line": self.line}
            )

        key = self.stdin[self.index]

        if key == ".":
            token = self.lex_dotwords()
            if token:
                return token

        if key == '"':
            token = self.lex_string()
            if token:
                return token

        if self.isAlphaOrOP(key):
            token = self.lex_alpha()
            if token:
                return token

        if key.isnumeric():
            token = self.lex_number()
            if token:
                return token

        token = self.lex_keychar(key)
        if token:
            return token

        token = self.lex_chars(key)
        if token:
            return token

        self.index += 1
        return self.lex()
