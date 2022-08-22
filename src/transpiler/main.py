import ast
from .lex import Lexer
from .parser import Parser
from .code import CodeGen

class Transpiler:
  stdin     = ''
  stdout    = ''
  lexer     = None 
  parser    = None 
  codegen   = None 
  ast       = []

  def __init__(self, stdin):
    self.stdin    = stdin
    self.lexer    = Lexer(stdin)
    self.parser   = Parser(self.lexer)
    self.codegen  = CodeGen()

  def run(self):
    self.parser.run()
    self.codegen.run(self.parser.ast)
    self.stdout   = self.codegen.stdout