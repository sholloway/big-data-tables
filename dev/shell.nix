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

pkgs.mkShell {
  name = "big-tables";
  buildInputs = [ 
    pkgs.git
    pkgs.gnumake
    (pkgs.python311.withPackages (ps:
      with ps; [
        pip
      ]))    
  ];
}