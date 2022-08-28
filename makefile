PYTHON=python3

conds: 
	$(PYTHON) src/lpp.py './examples/conds.lpp'

io: 
	$(PYTHON) src/lpp.py './examples/io.lpp'

vars: 
	$(PYTHON) src/lpp.py './examples/vars.lpp'

clean: 
	rm -rf build
	rm src/*.c
	rm src/transpiler/*.c
