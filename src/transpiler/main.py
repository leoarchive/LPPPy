# 
# This file is part of the LPP runtime distribution (https://github.com/fmleo/lpppy).
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
from .lex import Lexer
from .parser import Parser
from .code import CodeGen

class Transpiler:
  stdin     =   ''
  stdout    =   ''
  lexer     =   None 
  parser    =   None 
  codegen   =   None 
  tokens    =   []

  def __init__(self, stdin):
    self.stdin    =   stdin
    self.lexer    =   Lexer(stdin)
    self.parser   =   Parser(self.lexer)
    self.codegen  =   CodeGen()

  def run(self):
    self.parser.run()
    self.codegen.run(self.parser.tokens)
    self.stdout   =   self.codegen.stdout