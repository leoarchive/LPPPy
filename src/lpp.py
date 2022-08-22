from transpiler.main import Transpiler
from pathlib import Path
txt = Path('./examples/variables.lpp').read_text()
class LPP:
  transpiler = None

  def __init__(self):
    self.transpiler = Transpiler(txt)
    self.transpiler.run()
    print(self.transpiler.stdout)

LPP()