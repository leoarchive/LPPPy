from .lex import Lexer

class Transpiler:
  stdin = ''

  def __init__(self, stdin):
    self.stdin = stdin
    self.lexer = Lexer(stdin)
    print(self.lexer.lex().__dict__)
    print(self.lexer.lex().__dict__)
