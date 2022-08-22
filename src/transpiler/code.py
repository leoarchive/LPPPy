from operator import index

from transpiler.token import TokenTypes


class CodeGen:
  ast     = []
  index   = 0
  stdout  = ''

  def run(self, ast):
    self.ast = ast
    self.initialPipeline()

  def getDType(self, key):
    match key:
      case 'caractere':   return "''" 
      case 'real':        return "0" 

  def initialPipeline(self):
    self.stdout   =   f'# programa {self.ast[self.index].key}\n\n'
    self.stdout   +=  '# var\n'
    self.index    +=  1
    self.varBlock()

  def varBlock(self):
    while self.ast[self.index].type != TokenTypes.inicio:
      self.stdout += f'{self.ast[self.index].key} = {self.getDType(self.ast[self.index + 1].key)}\n'
      self.index  += 2
    
    self.inicioBlock()

  def inicioBlock(self):
    self.stdout   +=  '\n# inicio\n'
    self.index    += 1
    token = self.ast[self.index]
    match token.type:
      case TokenTypes.fim:
        self.stdout   +=  '\n# fim\n'