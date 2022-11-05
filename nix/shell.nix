with import <nixpkgs> {};

pkgs.mkShell {
  name = "nix-lpp-environment";
  version = "1.0.0";

  buildInputs = [
    python310
    python310Packages.black
    python310Packages.cython
  ];
}
 