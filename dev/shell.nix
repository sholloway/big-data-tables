# Installs my preferred tooling for working on this project.
# Neovim and Plugins

# TODO
  # Git
  # Apache Iceberg
  # Presto
  # Parquet?
  # Spark?
  # Apache Arrow

# To run:
# make nix

{pkgs ? import <nixpkgs> {}}:

let my_zulu = pkgs.callPackage ./zulu.nix { };
in
pkgs.mkShell {
  name = "big-tables";
  buildInputs = [ 
    pkgs.git
    pkgs.gnumake
    (pkgs.python311.withPackages (ps:
      with ps; [
        pip
      ])) 
    my_zulu  
  ];
}