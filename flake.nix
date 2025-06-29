{
  description = "SSP";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python312.withPackages (ps: with ps; [
          pip
          setuptools
          wheel
          pynvim  # Neovim Python integration
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv

            # OpenCV imshow GUI dependencies
            pkgs.zlib
            pkgs.libglvnd
            pkgs.glib
            pkgs.qt5.full
            pkgs.xorg.libxcb
            pkgs.xorg.xcbutil
            pkgs.fontconfig
            pkgs.freetype
            pkgs.libxkbcommon
            
            # C++ runtime needed for OpenCV (libstdc++.so.6)
            pkgs.stdenv.cc.cc
            pkgs.gcc.cc.lib
            # Neovim editor
            pkgs.neovim
          ];

          shellHook = ''
            # Setup Python virtualenv if not present
            if [ ! -d "./venv" ]; then
              python -m venv ./venv
            fi
            source ./venv/bin/activate

            # OpenCV + Qt5 plugin support
              export QT_QPA_PLATFORM_PLUGIN_PATH=${pkgs.qt5.qtbase.bin}/lib/qt-5/plugins
            export QT_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/lib/qt-5/plugins"

            # Fix all runtime libraries for OpenCV GUI & C++
            export LD_LIBRARY_PATH="${pkgs.zlib}/lib:\
${pkgs.libglvnd}/lib:\
${pkgs.glib.out}/lib:\
${pkgs.qt5.qtbase}/lib:\
${pkgs.xorg.libxcb}/lib:\
${pkgs.stdenv.cc.cc}/lib:\
$LD_LIBRARY_PATH"
  export LD_LIBRARY_PATH="${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH"
            # Ensure Neovim uses user config
            export XDG_CONFIG_HOME="$HOME/.config"

            echo "✅ venv activated | OpenCV imshow ready | Neovim using ~/.config/nvim"
          '';
        };
      });
}

