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
  ];
}

# Get Apache Iceberg directly from its repo since it's not in the Nix repo
pkgs.stdenv.mkDerivation {
  name = "iceberg";
  src = pkgs.fetchurl {
    url = "https://github.com/kopeio/kexpand/releases/download/0.2/kexpand-linux-amd64";
    sha256 = "0ldh303r5063kd5y73hhkbd9v11c98aki8wjizmchzx2blwlipy7";
  };
  phases = ["installPhase" "patchPhase"];
  installPhase = ''
    mkdir -p $out/bin
    cp $src $out/bin/kexpand
    chmod +x $out/bin/kexpand
  '';
}