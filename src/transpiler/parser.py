import ast
from .error import Error, ErrorTypes
from .token import TokenTypes
class Parser:
  token   = None
  lexer   = None
  ignore  = [TokenTypes.programa, TokenTypes.var, TokenTypes.colon]
  ast     = []

  def __init__(self, lexer):
    self.lexer = lexer

  def run(self):
    self.initialPipeline()

  def initialPipeline(self):
    self.checkToken(self.lexer.lex(), TokenTypes.programa)
    self.checkToken(self.lexer.lex(), TokenTypes.id)
    self.checkToken(self.lexer.lex(), TokenTypes.var)
    self.varBlock(self.lexer.lex())

  def varBlock(self, token):
    if (token.type == TokenTypes.inicio): 
      self.checkToken(token, TokenTypes.inicio)
      return self.inicioBlock()
    self.checkToken(token, TokenTypes.id)
    self.checkToken(self.lexer.lex(), TokenTypes.colon)
    self.checkToken(self.lexer.lex(), TokenTypes.dType)
    self.varBlock(self.lexer.lex())
   
  def inicioBlock(self):
    token = self.lexer.lex()
    match token.type:
      case TokenTypes.fim:
        self.checkToken(token, TokenTypes.fim)

  def checkToken(self, token, expectedType):
    if (not token or token.type != expectedType): 
      raise Error(ErrorTypes.parser_unexpected_token, token)

    if (not token.type in self.ignore):
      self.ast.append(token)