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
