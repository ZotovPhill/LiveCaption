.PHONY: help install lint format test run build run-docker clean

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  check-tools Verify that essential tools are installed"
	@echo "  install    Install the project dependencies (prod and dev extras)"
	@echo "  lint       Run code linting with Ruff"
	@echo "  format     Automatically fix lint issues with Ruff"
	@echo "  test       Run the test suite with pytest"
	@echo "  run        Launch the application with uvicorn (production mode)"
	@echo "  build      Build the Docker image for production deployment"
	@echo "  run-docker Run the application inside a Docker container"
	@echo "  clean      Remove __pycache__ and other temporary build artifacts"
	@echo "  pre-commit Install pre-commit hooks for code formatting and linting"


# Target to verify essential tools are in PATH.
# Documentation links for installation:
#   ruff:        https://docs.astral.sh/ruff/installation/
#   uvicorn:     https://www.uvicorn.org/deployment/
#   pre-commit:  https://pre-commit.com/#installation
#   pytest:      https://docs.pytest.org/en/stable/getting-started.html
#   docker:      https://docs.docker.com/get-docker/
#  	uv:          https://docs.astral.sh/uv/getting-started/installation/
check-tools:
	@echo "Checking required tools..."
	@command -v ruff >/dev/null 2>&1 || { echo >&2 "ERROR: ruff is not installed. See https://docs.astral.sh/ruff/installation/"; exit 1; }
	@command -v uvicorn >/dev/null 2>&1 || { echo >&2 "ERROR: uvicorn is not installed. See https://www.uvicorn.org/deployment/"; exit 1; }
	@command -v pre-commit >/dev/null 2>&1 || { echo >&2 "ERROR: pre-commit is not installed. See https://pre-commit.com/#installation"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo >&2 "ERROR: docker is not installed. See https://docs.docker.com/get-docker/"; exit 1; }
	@command -v pytest >/dev/null 2>&1 || { echo >&2 "ERROR: pytest is not installed. See https://docs.pytest.org/en/stable/getting-started.html"; exit 1; }
	@command -v uv >/dev/null 2>&1 || { echo >&2 "ERROR: uv is not installed. See https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
	@echo "All tools are installed."

install:
	@echo "Installing production and development dependencies..."
	# Assumes that your setup supports extra "dev" dependencies.
	 uv pip install -e .[dev]

lint:
	@echo "Running linting..."
	ruff check .

format:
	@echo "Running autoformatting..."
	ruff check . --fix

test:
	@echo "Running tests..."
	pytest

run:
	@echo "Starting Uvicorn..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info

build:
	@echo "Building Docker image..."
	docker build -t live-captions .

run-docker:
	@echo "Running Docker container..."
	docker run --rm -p 8000:8000 live-captions

clean:
	@echo "Cleaning up build artifacts..."
	# Remove Python bytecode caches and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build dist *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache

pre-commit:
	@echo "Installing pre-commit hooks..."
	pre-commit install
