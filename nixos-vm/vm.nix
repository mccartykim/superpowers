let
  nixpkgs = builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz";
  };

  nixos = import "${nixpkgs}/nixos" {
    configuration = ./configuration.nix;
  };
in
  nixos.vm
