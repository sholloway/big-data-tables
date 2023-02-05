# big-data-tables
This repo is a set of experiments working with a variety of big data tables.
It leverages the Nix package manager for handling dependencies.

## Getting Started
1. Install the [Nix package manager](https://nixos.org/manual/nix/stable/installation/installing-binary.html).
2. Using nix, install the project dependencies.
```shell
make nix setup
```
3. Activate the virtual environment.
```shell
source .venv/bin/activate
```
4. Run a script.
```shell
python scripts/spike.py
```

## Install Woes
If installing on Mac's with an M1 I've ran into issues with Nix getting confused
with Clang and local C++ libraries when trying to install Python wheels with
C extensions. To get around this, I've found the following process to work.
1. Install dependencies. `make nix`
2. Exit out of the nix shell. `exit`
3. Activate the virtual environment. `source .venv/bin/activate`
4. Install the Python dependencies using the OS installed clang. `pip install -r requirements.txt`
5. Then when working, just enable the nix shell. `make nix`

## Resources
- [Apache Spark](https://spark.apache.org/)
- [Apache Iceberg Source](https://github.com/apache/iceberg)
