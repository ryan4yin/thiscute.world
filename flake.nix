{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.11";
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    pre-commit-hooks,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      checks = {
        pre-commit-check = pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            typos.enable = true; # Source code spell checker
            alejandra.enable = true; # Nix linter
            prettier.enable = true; # Markdown & TS formatter
          };
          settings = {
            typos = {
              write = true; # Automatically fix typos
              configPath = "./.typos.toml";
            };
            prettier = {
              write = true; # Automatically format files
              configPath = "./.prettierrc.yaml";
            };
          };
        };
      };

      devShells.default = pkgs.mkShell {
        packages = with pkgs;
          [
            # Python development
            python311
            virtualenv

            # Nix-related
            alejandra
            deadnix
            statix
            # spell checker
            typos
            # code formatter
            nodePackages.prettier
          ]
          ++ (with pkgs.python311Packages; [
            pip
            pyyaml
          ]);

        shellHook = ''
          ${pkgs.python311}/bin/python --version
          ${self.checks.${system}.pre-commit-check.shellHook}
        '';
      };
    });
}
