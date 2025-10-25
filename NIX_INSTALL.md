# Install Nix

```bash
curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

Installation creates `/nix`, adds `nixbld` users, modifies shell profiles. May error at end but still works.

Find nix binary:
```bash
ls /nix/store/ | grep "nix-2"
# Use: /nix/store/<hash>-nix-<version>/bin/nix
```

## Usage

Run package once:
```bash
/nix/store/<hash>-nix-<version>/bin/nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz -p cowsay --run "cowsay hello"
```

Interactive shell:
```bash
/nix/store/<hash>-nix-<version>/bin/nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz -p cowsay
```
