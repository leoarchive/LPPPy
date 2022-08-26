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
import sys
from enum import Enum

class ErrorTypes(Enum):
  lexer_unexpected_token = 1
  parser_unexpected_token = 2

class Error:
  def __init__(self, type, token):
    if (not token): exit()
    print(f"{self.getMsg(type)} '{token.key}' na linha {token.line}\n", file=sys.stderr)

  def getMsg(self, type):
    match type:
      case ErrorTypes.lexer_unexpected_token:
        return 'lexer: token inesperado'
      case ErrorTypes.parser_unexpected_token:
        return 'parser: token inesperado'
