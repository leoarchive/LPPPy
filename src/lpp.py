#
# This file is part of the LPPPy distribution (https://github.com/leozamboni/LPPPy).
# Copyright (c) 2022 Leonardo Z. N.
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
import os


class LPP:
    transpiler = None
    file = sys.argv[1]

    def __init__(self):
        self.transpiler = Transpiler(Path(self.file).read_text())
        self.transpiler.run()

        if (not os.path.exists('build')):
            os.mkdir('build')
        
        print(self.file)
        build = open(f"build/{Path(self.file).name.split('.')[0]}.py", "w")
        build.write(self.transpiler.stdout)
        build.close

LPP()
