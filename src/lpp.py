from transpiler.main import Transpiler

class LPP:
  transpiler = None

  def __init__(self):
    self.transpiler = Transpiler('programa Exemplo \n')
    self.transpiler.run()

LPP()