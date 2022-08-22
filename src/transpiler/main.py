from .lex import Lexer
from .parser import Parser

class Transpiler:
  stdin   = ''
  lexer   = None 
  parser  = None 

  def __init__(self, stdin):
    self.stdin  = stdin
    self.lexer  = Lexer(stdin)
    self.parser = Parser(self.lexer)

  def run(self):
    self.parser.run()

    # print(self.lexer.lex().__dict__)
    # print(self.lexer.lex().__dict__)
