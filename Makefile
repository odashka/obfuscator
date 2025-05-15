# Makefile for Obfuscator development/test environment on macOS

PYTHON := python3

.DEFAULT_GOAL := help

help:
	@echo "Usage:"
	@echo "  make install_deps     Install Homebrew and Python dependencies"
	@echo "  make install_local    Install package locally"
	@echo "  make start_localstack Start LocalStack via Docker"
	@echo "  make stop_localstack  Stop LocalStack"
	@echo "  make test_unit        Run unit tests"
	@echo "  make test_integration Run integration tests"
	@echo "  make test_all         Run all tests with verbose output"

install_local:
	pip install .

install_deps:
	brew install --cask docker || true
	brew install localstack || true
	brew install localstack/tap/localstack-cli || true
	brew install awscli-local || true
	pip install -e .[dev]

start_localstack:
	open -a Docker
	localstack start -d
	localstack status services

stop_localstack:
	localstack stop

test_unit:
	pytest tests/unit/test_main.py

test_integration: start_localstack
	export PYTHONPATH=$$PWD && pytest tests/integration/test_main_localstack.py

test_all: start_localstack
	pytest -vvvrP tests
