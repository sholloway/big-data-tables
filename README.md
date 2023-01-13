# big-data-tables
This repo is a set of experiments working with a variety of big data tables.
It leverages the Nix package manager for handling dependencies.

# Getting Started
1. Install the [Nix package manager](https://nixos.org/manual/nix/stable/installation/installing-binary.html).
2. Using nix, install the project dependencies.
```shell
make install
```
3. Activate the virtual environment.
```shell
source .venv/bin/activate
```
4. Run a script.
```shell
python scripts/spike.py
```

# Resources
- [Apache Spark](https://spark.apache.org/)
- [Apache Iceberg Source](https://github.com/apache/iceberg)
