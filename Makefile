.PHONY: install
install:
	pip3 install poetry
	poetry install

.PHONY: lint
lint: install
	poetry run tox -e lint

.PHONY: format
format: install
	poetry run black src test
	poetry run isort src test

.PHONY: format-check
format-check: install
	poetry run black src test --check
	poetry run isort src test --check

.PHONY: unit
unit: install
	poetry run tox -e test_cov $(OPTIONS)

.PHONY: test
test: install
	poetry run tox

.PHONY: build
build: install
	poetry version $$(git describe --tags --abbrev=0)
	poetry build
