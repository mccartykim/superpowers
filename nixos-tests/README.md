# NixOS Integration Tests with Cowsay

This directory contains NixOS integration tests demonstrating VM testing with the NixOS testing framework.

## Tests

### 1. Cowsay Hello World (`cowsay-hello`)
Tests a single NixOS VM running cowsay:
- Boots a minimal NixOS VM
- Runs `cowsay "Hello from NixOS VM!"`
- Verifies the output contains expected text and the ASCII cow

### 2. VM Network Ping Test (`vm-network-ping`)
Tests two VMs on a network:
- Creates `server` and `client` VMs on a shared network
- Tests bidirectional ping connectivity
- Runs cowsay on both machines
- Verifies network communication and services

## Running the Tests

### Prerequisites

These tests require:
- Nix with flakes enabled
- Multi-user Nix installation OR
- Docker with the `nixos/nix` image

### Option 1: With Local Nix (Multi-user)

```bash
# Check all tests
nix flake check

# Build and run specific test
nix build .#checks.x86_64-linux.cowsay-hello
nix build .#checks.x86_64-linux.vm-network-ping

# Run interactive test (for debugging)
nix run .#packages.x86_64-linux.test-cowsay-hello
nix run .#packages.x86_64-linux.test-vm-network
```

### Option 2: With Docker or Podman

```bash
# Run tests in Nix container (Docker)
docker run --rm -it -v $PWD:/workspace -w /workspace \
  nixos/nix nix --extra-experimental-features "nix-command flakes" \
  flake check

# Or with Podman (recommended for rootless environments)
podman run --rm -v $PWD:/workspace:Z -w /workspace \
  docker.io/nixos/nix:latest nix --extra-experimental-features "nix-command flakes" \
  flake check

# Build specific test
podman run --rm -v $PWD:/workspace:Z -w /workspace \
  docker.io/nixos/nix:latest nix --extra-experimental-features "nix-command flakes" \
  build .#checks.x86_64-linux.cowsay-hello
```

**Note**: Podman is often preferred in rootless or restricted environments as it's daemonless and more secure.

## Test Structure

```nix
checks.${system} = {
  cowsay-hello = pkgs.nixosTest {
    name = "cowsay-hello-world";
    nodes.machine = { ... };  # VM configuration
    testScript = '' ... '';    # Python test script
  };

  vm-network-ping = pkgs.nixosTest {
    name = "two-vms-ping";
    nodes = {
      server = { ... };
      client = { ... };
    };
    testScript = '' ... '';
  };
};
```

## Known Limitations

- Requires KVM/hardware virtualization for best performance
- Single-user Nix installations may have issues with complex VM builds
- Nested virtualization environments may not support these tests

## References

- [NixOS Integration Testing Documentation](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html)
- [NixOS Testing Library](https://nixos.wiki/wiki/NixOS_Testing_library)
- [Example Tests in nixpkgs](https://github.com/NixOS/nixpkgs/tree/master/nixos/tests)
