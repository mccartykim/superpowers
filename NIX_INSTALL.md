# Nix Installation

## Install
```bash
curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

## Run a package without installing
```bash
nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz -p <package> --run "<command>"
```

## Example
```bash
nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz -p cowsay --run "cowsay hello"
```

## Enter interactive shell with package
```bash
nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz -p <package>
```

## Notes
- First run downloads packages (slow)
- Cached in `/nix/store` (fast after)
- Installs to `/nix`, creates `nixbld` users
- May fail on last step (profile setup) but still works
