with import <nixpkgs> {};

let
  script = pkgs.writeShellScriptBin "start" 
  ''
    steam-run $(which bun) dev
  '';
in
  pkgs.mkShell {
    name = "nix-lpp-environment";
    version = "1.0.0";

    nativeBuildInputs = [ 
      bun
      script
    ];

    buildInputs = [
      python27
    ];
  }
 