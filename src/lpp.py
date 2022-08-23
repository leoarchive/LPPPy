from transpiler.main import Transpiler
from pathlib import Path

class LPP:
  transpiler = None

  def __init__(self):
    self.transpiler = Transpiler(Path('./examples/input-output.lpp').read_text())
    self.transpiler.run()
    print(self.transpiler.stdout)

LPP()