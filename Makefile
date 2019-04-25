clean:
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +
	find . -name 'pip-wheel-metadata' -exec rm -fr {} +
	find . -name 'tenark.egg-info' -exec rm -fr {} +

test:
	pytest

coverage: 
	mypy tenark
	pytest -x --cov=tenark tests/ --cov-report term-missing -s

PART ?= patch

version:
	bump2version $(PART) pyproject.toml tenark/__init__.py --tag --commit
