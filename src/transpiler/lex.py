from .error import Error, ErrorTypes
from .token import Token, TokenTypes

class Lexer:
  stdin     = ''
  index     = 0
  line      = 0
  keyWords  = ['programa']
  operators = ['←','→']
  chars     = ['\n']
  
  def __init__(self, stdin):
    self.stdin = stdin

  def lex_string(self):
    start = self.index
    while len(self.stdin) > self.index and self.stdin[self.index].isalpha():
      self.index += 1

    key   = self.stdin[start:self.index]
    token = self.lex_keyword(key)
    if (token): return token
    return Token(key, TokenTypes.id, self.line)

  def lex_number(self):
    start = self.index
    while len(self.stdin) > self.index and self.stdin[self.index].isnumeric():
      self.index += 1

    key   = self.stdin[start:self.index]
    return Token(key, TokenTypes.numb, self.line)

  def lex_keyword(self, key):
    for keyWord in self.keyWords:
      if (key == keyWord): 
        return Token(key, Token.getType(key), self.line)

  def lex_operator(self, key):
    for operator in self.operators:
      if (key == operator): 
        return Token(key, Token.getType(key), self.line)

  def lex_chars(self, key):
    for char in self.chars:
      if (key == char): 
        match key:
          case '\n':
            self.line += 1
            return Token(key, TokenTypes.bLine, self.line)

  def lex(self):
    if (len(self.stdin) < self.index): 
      raise Error(ErrorTypes.lexer_unexpected_token, "EOF", self.line)
      
    key = self.stdin[self.index]
 
    if (key.isalpha()):
      token = self.lex_string()
      if (token): return token

    if (key.isnumeric()):
      token = self.lex_number()
      if (token): return token

    token = self.lex_operator(key)
    if (token): return token

    token = self.lex_chars(key)
    if (token): return token

    self.index += 1
    return self.lex()
        