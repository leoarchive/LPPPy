# 
# This file is part of the LPPPy distribution (https://github.com/fmleo/lpppy).
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
from .error import Error, ErrorTypes
from .token import TokenKeys, TokenTypes

# Não há necessidade de armazenar tokens que não serão necessários para
# a geracão do código final, tal qual 'programa', 'var', ':', '[', ...
# 
# Caso no decorrer do desenvolvimento haja necessidade, a geracão de código
# python deve ser inteiramente refatorada.
class Parser:
  token   =   None
  lexer   =   None
  tokens  =   []
  ignore  =   [TokenTypes.programa, 
              TokenTypes.var, 
              TokenTypes.colon, 
              TokenTypes.rSquare, 
              TokenTypes.lSquare,
              TokenTypes.dPeriod,
              TokenTypes.de]

  def __init__(self, lexer):  self.lexer = lexer

  def run(self):              self.parse()

  def eatToken(self, token, expectedType):
    if (not token or token.type != expectedType): 
      raise Error(ErrorTypes.parser_unexpected_token, token)

    if (not token.type in self.ignore):
      self.tokens.append(token)

  def parse(self):
    self.eatToken(self.lexer.lex(), TokenTypes.programa)
    self.eatToken(self.lexer.lex(), TokenTypes.id)
    self.eatToken(self.lexer.lex(), TokenTypes.var)
    self.parseVarBlock(self.lexer.lex())

  def parseVarBlock(self, token):
    if (token.type == TokenTypes.inicio): 
      self.eatToken(token, TokenTypes.inicio)
      return self.parseBlock()
    self.eatToken(token, TokenTypes.id)

    token = self.lexer.lex()
    if (token.type == TokenTypes.dot):
      while token.type == TokenTypes.dot:
        self.eatToken(token, TokenTypes.dot)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        token = self.lexer.lex()

    self.eatToken(token, TokenTypes.colon)

    token = self.lexer.lex()
    self.eatToken(token, TokenTypes.dType)
    if (token.key == TokenKeys.conjunto):
      self.eatToken(self.lexer.lex(), TokenTypes.lSquare)
      self.eatToken(self.lexer.lex(), TokenTypes.numb)
      self.eatToken(self.lexer.lex(), TokenTypes.dPeriod)
      self.eatToken(self.lexer.lex(), TokenTypes.numb)
      self.eatToken(self.lexer.lex(), TokenTypes.rSquare)
      self.eatToken(self.lexer.lex(), TokenTypes.de)
      self.eatToken(self.lexer.lex(), TokenTypes.dType)

    self.parseVarBlock(self.lexer.lex())
   
  def parseBlock(self):
    token = self.lexer.lex()
    while True:
      match token.type:
        case TokenTypes.fim:      return  self.eatToken(token, TokenTypes.fim) 
        case TokenTypes.leia:     token = self.parseLeia(token)
        case TokenTypes.escreva:  token = self.parseEscreva(token)

  def parseLeia(self, token):
    self.eatToken(token, TokenTypes.leia)
    self.eatToken(self.lexer.lex(), TokenTypes.id)
    token = self.lexer.lex()
    if (token.type == TokenTypes.dot):
      while token.type == TokenTypes.dot:
        self.eatToken(token, TokenTypes.dot)
        self.eatToken(self.lexer.lex(), TokenTypes.id)
        token = self.lexer.lex()
    return token
  
  def parseEscreva(self, token):
    self.eatToken(token, TokenTypes.escreva)

    token = self.lexer.lex()
    match token.type:
      case TokenTypes.str:
        self.eatToken(token, TokenTypes.str)
      case TokenTypes.id:
        self.eatToken(token, TokenTypes.id)

    token = self.lexer.lex()
    if (token.type == TokenTypes.dot):
      while token.type == TokenTypes.dot:
        self.eatToken(token, TokenTypes.dot)
        token = self.lexer.lex()
        match token.type:
          case TokenTypes.str:
            self.eatToken(token, TokenTypes.str)
          case TokenTypes.id:
            self.eatToken(token, TokenTypes.id)
            
        token = self.lexer.lex()

    return token