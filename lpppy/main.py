from lpppy.compiler.main import Compiler
from types import SimpleNamespace
from pathlib import Path
import sys
import os


class LPP:
    compiler = None
    file = None
    config = SimpleNamespace(debug=False)

    def __init__(self):
        if len(sys.argv) <= 1:
            sys.tracebacklimit = 0
            print("nothing to do!")
            exit(0)
        else:
            self.file = sys.argv[1]

        if len(sys.argv) > 2:
            if sys.argv[1] == "--debug-mode":
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

        exit(0)
