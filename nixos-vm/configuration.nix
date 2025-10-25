{ config, pkgs, ... }:

{
  # Basic VM configuration
  imports = [];

  # Enable serial console for VM
  boot.kernelParams = [ "console=ttyS0" ];

  # Minimal system configuration
  services.getty.autologinUser = "root";

  # Network configuration
  networking.hostName = "cowsay-vm";
  networking.firewall.enable = false;

  # Add cowsay package
  environment.systemPackages = with pkgs; [
    cowsay
    vim
  ];

  # Create a systemd service that runs cowsay
  systemd.services.cowsay-service = {
    description = "Cowsay Hello Service";
    wantedBy = [ "multi-user.target" ];
    serviceConfig = {
      Type = "oneshot";
      RemainAfterExit = true;
      ExecStart = "${pkgs.bash}/bin/bash -c '${pkgs.cowsay}/bin/cowsay \"Hello from NixOS VM!\" > /var/log/cowsay-output.txt'";
    };
  };

  # Create a periodic cowsay service that runs every minute
  systemd.services.cowsay-periodic = {
    description = "Periodic Cowsay Service";
    serviceConfig = {
      Type = "oneshot";
      ExecStart = "${pkgs.bash}/bin/bash -c '${pkgs.cowsay}/bin/cowsay \"Mooo! The time is $(date)\" >> /var/log/cowsay-periodic.txt'";
    };
  };

  systemd.timers.cowsay-periodic = {
    description = "Run cowsay every minute";
    wantedBy = [ "timers.target" ];
    timerConfig = {
      OnBootSec = "10s";
      OnUnitActiveSec = "60s";
    };
  };

  # Enable logging to console
  services.journald.extraConfig = ''
    ForwardToConsole=yes
  '';

  system.stateVersion = "24.05";
}
