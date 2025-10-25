{
  description = "NixOS VM integration tests with cowsay";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      # Test 1: Single VM running cowsay
      checks.${system} = {
        cowsay-hello = pkgs.nixosTest {
          name = "cowsay-hello-world";

          nodes.machine = { config, pkgs, ... }: {
            environment.systemPackages = [ pkgs.cowsay ];
          };

          testScript = ''
            machine.wait_for_unit("multi-user.target")
            output = machine.succeed("cowsay 'Hello from NixOS VM!'")
            print(output)
            assert "Hello from NixOS VM!" in output
            assert "moo" in output.lower() or "^__^" in output
          '';
        };

        # Test 2: Two VMs pinging each other
        vm-network-ping = pkgs.nixosTest {
          name = "two-vms-ping";

          nodes = {
            server = { config, pkgs, ... }: {
              networking.firewall.enable = false;
              environment.systemPackages = [ pkgs.cowsay ];
            };

            client = { config, pkgs, ... }: {
              networking.firewall.enable = false;
              environment.systemPackages = [ pkgs.cowsay ];
            };
          };

          testScript = ''
            start_all()

            # Wait for both machines to be ready
            server.wait_for_unit("multi-user.target")
            client.wait_for_unit("multi-user.target")

            # Get IP addresses
            server_ip = server.succeed("ip -4 addr show eth1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'").strip()
            client_ip = client.succeed("ip -4 addr show eth1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'").strip()

            print(f"Server IP: {server_ip}")
            print(f"Client IP: {client_ip}")

            # Test ping from client to server
            client.succeed(f"ping -c 3 {server_ip}")
            print("✓ Client can ping server")

            # Test ping from server to client
            server.succeed(f"ping -c 3 {client_ip}")
            print("✓ Server can ping client")

            # Bonus: Run cowsay on both machines
            server_cowsay = server.succeed("cowsay 'I am the server!'")
            client_cowsay = client.succeed("cowsay 'I am the client!'")

            print("Server says:")
            print(server_cowsay)
            print("Client says:")
            print(client_cowsay)

            assert "I am the server!" in server_cowsay
            assert "I am the client!" in client_cowsay
          '';
        };
      };

      # Make tests easily runnable
      packages.${system} = {
        test-cowsay-hello = self.checks.${system}.cowsay-hello.driverInteractive;
        test-vm-network = self.checks.${system}.vm-network-ping.driverInteractive;
      };
    };
}
