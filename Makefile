# Launch a Nix shell for doing development in.
nix:
	nix-shell --run zsh ./dev/shell.nix

# Create a Python virtual environment and install all the dependencies
blah:
	@( \
	set -e ; \
	python -m venv ./.venv; \
	source .venv/bin/activate; \
	pip install -r requirements.txt; \
	)