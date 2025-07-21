# Makefile 

.PHONY: lint lint-black lint-isort lint-flake test format

## Whole lint 
lint: lint-black lint-isort lint-flake 

## Black: code style (PEP8)
lint-black:
	@echo "Running black..."
	@black . --check 

## isort: import order 
lint-iosrt:
	@echo "Running isort..."
	@isort . --check-only

## flake8: grammer/style 
lint-flake:
	@echo "Running flake8..."
	@flake8 .

## test 
test:
	@echo "Running pytest..."
	@TEST_MODE=1 pytest -v --disable-warnings

## re format using lint
format: 
	@echo "Running black and isort(auto-fix)..."
	@black . 
	@isort .