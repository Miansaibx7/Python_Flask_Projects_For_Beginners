.PHONY: help install sync dev run test lint format check shell clean

PYTHON := uv run python
FLASK := uv run flask
PYTEST := uv run pytest
RUFF := uv run ruff

help:
	@echo "Flask Project Commands"
	@echo "======================"
	@echo "make install  - Install dependencies"
	@echo "make sync     - Synchronize uv environment"
	@echo "make dev      - Start development server"
	@echo "make run      - Start Flask server"
	@echo "make test     - Run tests"
	@echo "make lint     - Check code with Ruff"
	@echo "make format   - Format code with Ruff"
	@echo "make check    - Run linting and tests"
	@echo "make shell    - Open Python shell"
	@echo "make clean    - Remove cache files"

install:
	uv sync

sync:
	uv sync

dev:
	$(FLASK) --app app run --debug

run:
	$(FLASK) --app app run

test:
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

check: lint test

shell:
	$(PYTHON)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type f -name "*.pyc" -delete