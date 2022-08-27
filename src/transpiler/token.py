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
from ast import NotEq
from enum import Enum


class TokenKeys:
    programa = "programa"
    var = "var"
    caractere = "caractere"
    real = "real"
    inicio = "início"
    fim = "fim"
    conjunto = "conjunto"
    entao = "então"
    senao = "senão"
    dPeriod = ".."
    de = "de"
    se = "se"
    inteiro = "inteiro"
    leia = "leia"
    escreva = "escreva"
    rArrow = "←"
    lArrow = "→"
    colon = ":"
    rSquare = "]"
    lSquare = "["
    dot = ","
    _and = ".E."
    _not = ".NÃO."
    _or = ".OU."
    graterEq = ">="
    lessEq = "<="
    less = "<"
    grater = ">"
    NotEq = "<>"
    equal = "="
    plus = "+"
    minus = "-"
    mult = "*"
    div = "/"
    rParen = ")"
    lParen = "("
    fimse = "fim_se"


class TokenTypes(Enum):
    id = 1
    numb = 2
    lArrow = 3
    rArrow = 4
    programa = 5
    var = 6
    colon = 7
    dType = 8
    inicio = 9
    fim = 10
    rSquare = 11
    lSquare = 12
    dPeriod = 13
    de = 14
    dot = 15
    leia = 16
    escreva = 17
    str = 18
    logicalOps = 19
    mathOps = 20
    se = 21
    lParen = 22
    rParen = 23
    entao = 24
    fimse = 25
    senao = 26
    conjunto = 27


class Token:
    key = ""
    type = 0
    line = 0

    def __init__(self, key, type, line):
        self.key = key
        self.type = type
        self.line = line

    def getType(key):
        if key == TokenKeys.var:
            return TokenTypes.var
        elif key == TokenKeys.programa:
            return TokenTypes.programa
        elif key == TokenKeys.inicio:
            return TokenTypes.inicio
        elif key == TokenKeys.leia:
            return TokenTypes.leia
        elif key == TokenKeys.escreva:
            return TokenTypes.escreva
        elif key == TokenKeys.fim:
            return TokenTypes.fim
        elif key == TokenKeys.se:
            return TokenTypes.se
        elif key == TokenKeys.entao:
            return TokenTypes.entao
        elif key == TokenKeys.senao:
            return TokenTypes.senao
        elif key == TokenKeys.fimse:
            return TokenTypes.fimse
        elif key == TokenKeys.rArrow:
            return TokenTypes.rArrow
        elif key == TokenKeys.lArrow:
            return TokenTypes.lArrow
        elif key == TokenKeys.colon:
            return TokenTypes.colon
        elif key == TokenKeys.dPeriod:
            return TokenTypes.dPeriod
        elif key == TokenKeys.dot:
            return TokenTypes.dot
        elif key == TokenKeys.rSquare:
            return TokenTypes.rSquare
        elif key == TokenKeys.lSquare:
            return TokenTypes.lSquare
        elif key == TokenKeys.rParen:
            return TokenTypes.rParen
        elif key == TokenKeys.lParen:
            return TokenTypes.lParen
        elif key == TokenKeys.de:
            return TokenTypes.de
        elif (
            key == TokenKeys.caractere
            or key == TokenKeys.real
            or key == TokenKeys.inteiro
            or key == TokenKeys.conjunto
        ):
            return TokenTypes.dType
        elif (
            key == TokenKeys._and
            or key == TokenKeys._or
            or key == TokenKeys._not
            or key == TokenKeys.grater
            or key == TokenKeys.graterEq
            or key == TokenKeys.less
            or key == TokenKeys.lessEq
            or key == TokenKeys.NotEq
            or key == TokenKeys.equal
        ):
            return TokenTypes.logicalOps
        elif (
            key == TokenKeys.plus
            or key == TokenKeys.minus
            or key == TokenKeys.mult
            or key == TokenKeys.div
        ):
            return TokenTypes.mathOps
        else:
            return TokenTypes.id
