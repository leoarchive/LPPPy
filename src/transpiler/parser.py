from .error import Error, ErrorTypes
from .token import TokenTypes
from .lex import Lexer
class Parser:
  token = None
  lexer = None

  def __init__(self, lexer):
    self.lexer = lexer

  def run(self):
    self.initialPipeline()

  def initialPipeline(self):
    self.checkToken(self.lexer.lex(), TokenTypes.programa)
    self.checkToken(self.lexer.lex(), TokenTypes.id)
    self.checkToken(self.lexer.lex(), TokenTypes.bLine)

  def checkToken(self, token, expectedType):
    if (token.type != expectedType): 
      raise Error(ErrorTypes.lexer_unexpected_token, token.key, token.line)