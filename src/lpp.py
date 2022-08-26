# 
# This file is part of the LPPPy distribution (https://github.com/fmleo/lpppy).
# Copyright (c) 2022 IFRS - Campus Vacaria.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from transpiler.main import Transpiler
from pathlib import Path
import sys

class LPP:
  transpiler = None

  def __init__(self):
    self.transpiler = Transpiler(Path(sys.argv[1]).read_text())
    self.transpiler.run()
    print(self.transpiler.stdout)

LPP()