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
from types import SimpleNamespace
from compiler.main import Compiler
from pathlib import Path
import sys
import os


class LPP:
    compiler = None
    file = None
    config = SimpleNamespace(debug = False)

    def __init__(self):
        if len(sys.argv) <= 1:
            sys.tracebacklimit = 0
            raise print("nothing to do!")
        else:
            self.file = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[1] == '--debug-mode':
                self.file = sys.argv[2]
                self.config.debug = True
        else:
            sys.tracebacklimit = 0

        self.compiler = Compiler(Path(self.file).read_text())
        self.compiler.run()

        if self.config.debug:
            if not os.path.exists("build"):
                os.mkdir("build")

            build = open(f"build/{Path(self.file).name.split('.')[0]}.py", "w")
            build.write(self.compiler.stdout)
            build.close
        else:
            exec(self.compiler.stdout)


LPP()
