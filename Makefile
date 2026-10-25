.PHONY: setup lint format test check

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests

format:
	ruff check --fix src tests
	ruff format src tests

test:
	pytest

check: lint test
