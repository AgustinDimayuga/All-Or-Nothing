{
  description = "centralcoastcauldrons dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python312
            uv
            pkg-config
            postgresql
          ];

          shellHook = ''
            export UV_NO_MANAGED_PYTHON=1
            export UV_PYTHON="$(which python3)"

            echo "Python: $(python3 --version)"
            echo "uv: $(uv --version)"
            echo "uv will use: $UV_PYTHON"
            echo ""
            echo "First time setup:"
            echo "  uv venv --python \$UV_PYTHON"
            echo "  uv sync"
          '';
        };
      });
}
