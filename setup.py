from setuptools import setup
from Cython.Build import cythonize

files = [
  'src/lpp.py',
  'src/compiler/code.py',
  'src/compiler/error.py',
  'src/compiler/lex.py',
  'src/compiler/main.py',
  'src/compiler/parse.py',
  'src/compiler/symtab.py',
  'src/compiler/token.py',
]

setup(
    name='LPPPy',
    ext_modules=cythonize(files),
    zip_safe=False,
)