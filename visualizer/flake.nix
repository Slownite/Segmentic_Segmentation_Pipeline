{
  description = "Visualizer SSP";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
          opencv-with-gui = pkgs.opencv.override {
          enableGtk3 = true;  
          };
          in {
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "Visualizer"
          version = "0.1.0";
          src = ./.;

          buildInputs = [
            pkgs.gcc
            pkgs.gnumake
            opencv-with-gui
            pkgs.pkg-config
            pkgs.bear
            pkgs.onnxruntime
          ];

          buildPhase = "make";

          installPhase = ''
            mkdir -p $out/bin
            cp build/my-app $out/bin/
          '';
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.gcc
            pkgs.gnumake
            pkgs.pkg-config
            pkgs.gdb
            opencv-with-gui
            pkgs.bear
            pkgs.onnxruntime
          ];
        };
      });
}

