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