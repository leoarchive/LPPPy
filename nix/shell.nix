with import <nixpkgs> {};

let
  buildScript = pkgs.writeShellScriptBin "build" 
  ''
  PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)

  cython -3 src/compiler/*.py
  cython -3 src/lpp.py --embed
  rm src/compiler/__init__.c
 
  clang -Os $(python3-config --includes) src/lpp.c src/compiler/*.c -o src/lpppy $(python3-config --ldflags) -l$PYTHONLIBVER

  rm -rf build
	rm src/*.c
	rm src/compiler/*.c

  ln -s -f src/lpppy .
  '';
in
  pkgs.mkShell {
    name = "nix-lpp-environment";
    version = "1.0.0";

    nativeBuildInputs = [ 
      clang
      bun

      python310Packages.black
      python310Packages.cython
      
      buildScript
    ];

    buildInputs = [
      python310
    ];
  }
 