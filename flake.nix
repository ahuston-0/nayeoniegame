{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python313
              uv
            ];

            # SDL2 libraries needed for pygame
            buildInputs = with pkgs; [
              SDL2
              SDL2_image
              SDL2_mixer
              SDL2_ttf
              zlib  # Required for pygame font module
            ] ++ pkgs.lib.optionals pkgs.stdenv.isLinux [
              # Wayland support
              wayland
              wayland-protocols
              libxkbcommon
              # X11 support (for Xwayland)
              libX11
              libXcursor
              libXi
              libXrandr
              # EGL/OpenGL support for rendering
              libGL
              mesa
            ];

            shellHook = ''
              # Configure uv
              export UV_PYTHON=${pkgs.python313}/bin/python
              export UV_PYTHON_DOWNLOADS=never

              # For pygame display on Linux - ensure SDL can find system libraries
              ${pkgs.lib.optionalString pkgs.stdenv.isLinux ''
                export SDL_VIDEODRIVER=wayland,x11
                export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
                  pkgs.SDL2
                  pkgs.zlib
                  pkgs.wayland
                  pkgs.libxkbcommon
                  pkgs.libX11
                  pkgs.libXcursor
                  pkgs.libXi
                  pkgs.libXrandr
                  pkgs.libGL
                  pkgs.mesa
                ]}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
              ''}

              echo "nayeoniegame development environment"
              echo "Python: $(python --version)"
              echo "uv: $(uv --version)"
              echo ""
              echo "Run 'uv sync' to install dependencies"
              echo "Run game: uv run python -m nayeoniegame"
            '';
          };
        }
      );

      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.python313Packages.buildPythonApplication {
            pname = "nayeoniegame";
            version = "0.1.0";
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with pkgs.python313Packages; [
              hatchling
            ];

            propagatedBuildInputs = with pkgs.python313Packages; [
              pygame
            ];
          };
        }
      );
    };
}
