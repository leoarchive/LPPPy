from .error import Error, ErrorTypes
from .token import TokenKeys, TokenTypes

# Não há necessidade de armazenar tokens que não serão necessários para
# a geracão do código em final, tal qual 'programa', 'var', ':', '[', ...
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

    token = self.lexer.lex()
    if (token.type == TokenTypes.dot):
      while token.type != TokenTypes.colon:
        self.checkToken(token, TokenTypes.dot)
        self.checkToken(self.lexer.lex(), TokenTypes.id)
        token = self.lexer.lex()

    self.checkToken(token, TokenTypes.colon)

    token = self.lexer.lex()
    self.checkToken(token, TokenTypes.dType)
    if (token.key == TokenKeys.conjunto):
      self.checkToken(self.lexer.lex(), TokenTypes.lSquare)
      self.checkToken(self.lexer.lex(), TokenTypes.numb)
      self.checkToken(self.lexer.lex(), TokenTypes.dPeriod)
      self.checkToken(self.lexer.lex(), TokenTypes.numb)
      self.checkToken(self.lexer.lex(), TokenTypes.rSquare)
      self.checkToken(self.lexer.lex(), TokenTypes.de)
      self.checkToken(self.lexer.lex(), TokenTypes.dType)

    self.varBlock(self.lexer.lex())
   
  def inicioBlock(self):
    token = self.lexer.lex()
    match token.type:
      case TokenTypes.fim:  self.checkToken(token, TokenTypes.fim)

  def checkToken(self, token, expectedType):
    if (not token or token.type != expectedType): 
      raise Error(ErrorTypes.parser_unexpected_token, token)

    if (not token.type in self.ignore):
      self.tokens.append(token)