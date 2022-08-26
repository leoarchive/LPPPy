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

class TokenKeys():
 programa     =   'programa'
 var          =   'var'
 caractere    =   'caractere'
 real         =   'real'
 inicio       =   'início'
 fim          =   'fim'
 conjunto     =   'conjunto'
 entao        =   'então'
 senao        =   'senão'
 dPeriod      =   '..'
 de           =   'de'
 se           =   'se'
 inteiro      =   'inteiro'
 leia         =   'leia'
 escreva      =   'escreva'
 rArrow       =   '←',
 lArrow       =   '→',
 colon        =   ':',
 rSquare      =   ']',
 lSquare      =   '['
 dot          =   ','
 _and         =   '.E.'
 _not         =   '.NÃO.'
 _or          =   '.OU.'
 graterEq     =   '>='
 lessEq       =   '<='
 less         =   '<'
 grater       =   '>'
 NotEq        =   '<>'
 equal        =   '='
 plus         =   '+'
 minus        =   '-'
 mult         =   '*'
 div          =   '/'
 rParen       =   ')'
 lParen       =   '('
 fimse        =   'fim_se'

class TokenTypes(Enum):
  id          =   1
  numb        =   2
  lArrow      =   3
  rArrow      =   4
  programa    =   5
  var         =   6
  colon       =   7
  dType       =   8
  inicio      =   9
  fim         =   10
  rSquare     =   11
  lSquare     =   12
  dPeriod     =   13
  de          =   14
  dot         =   15
  leia        =   16
  escreva     =   17
  str         =   18
  logicalOps  =   19
  mathOps     =   20
  se          =   21
  lParen      =   22
  rParen      =   23
  entao       =   24
  fimse       =   25
  senao       =   26
  conjunto    =   27
  
class Token:
  key         =   ''
  type        =   0
  line        =   0

  def __init__(self, key, type, line):
    self.key  = key
    self.type = type
    self.line = line

  def getType(key):
    match key:
      case 'var':                 return TokenTypes.var
      case 'programa':            return TokenTypes.programa
      case 'início':              return TokenTypes.inicio
      case 'leia':                return TokenTypes.leia
      case 'escreva':             return TokenTypes.escreva
      case 'fim':                 return TokenTypes.fim
      case 'se':                  return TokenTypes.se
      case 'então':               return TokenTypes.entao
      case 'senão':               return TokenTypes.senao
      case 'fim_se':              return TokenTypes.fimse
      case '←':                   return TokenTypes.rArrow
      case '→':                   return TokenTypes.lArrow
      case ':':                   return TokenTypes.colon
      case '..':                  return TokenTypes.dPeriod
      case ',':                   return TokenTypes.dot
      case ']':                   return TokenTypes.rSquare
      case '[':                   return TokenTypes.lSquare
      case ')':                   return TokenTypes.rParen
      case '(':                   return TokenTypes.lParen
      case 'de':                  return TokenTypes.de
      case 'caractere' | 'real' | 'inteiro' | 'conjunto':  
                                  return TokenTypes.dType
      case '.E.' | '.OU.' | '.NÃO.' | '>' | '<' | '>=' | '<=' | '<>' | '=':  
                                  return TokenTypes.logicalOps
      case '+' | '-' | '*' | '/':
                                  return TokenTypes.mathOps
      case _:                     return TokenTypes.id