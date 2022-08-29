with import <nixpkgs> {};

let
  startScript = pkgs.writeShellScriptBin "start" 
  ''
    steam-run $(which bun) dev
  '';
  buildScript = pkgs.writeShellScriptBin "build" 
  ''
  PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)

  cython -3 src/transpiler/*.py
  cython -3 src/lpp.py --embed
  rm src/transpiler/__init__.c
 
  clang -Os $(python3-config --includes) src/lpp.c src/transpiler/*.c -o src/lpppy $(python3-config --ldflags) -l$PYTHONLIBVER

  make clean
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
      
      startScript
      buildScript
    ];

    buildInputs = [
      python310
    ];
  }
 