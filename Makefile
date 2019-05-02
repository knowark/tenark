clean:
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +
	find . -name 'pip-wheel-metadata' -exec rm -fr {} +
	find . -name 'tenark.egg-info' -exec rm -fr {} +

test:
	pytest

COVFILE ?= .coverage

coverage: 
	mypy tenark
	export COVERAGE_FILE=$(COVFILE); pytest -x --cov=tenark tests/ \
	--cov-report term-missing -s -o cache_dir=/tmp/.pytest_cache

PART ?= patch

version:
	bump2version $(PART) pyproject.toml tenark/__init__.py --tag --commit

devdeploy:
	# Run as root in the development server
	sudo apt update
	sudo apt install -y postgresql
	sudo apt install -y python3-pip
	sudo apt install -y postgresql-server-dev-all
	sudo python3 -m pip install mypy pytest pytest-cov psycopg2
	sudo id -u tenark &>/dev/null || sudo adduser --system \
	--home /opt/tenark --shell /bin/bash tenark
	sudo -u postgres dropdb --if-exists tenark
	sudo -u postgres dropuser --if-exists tenark
	sudo -u postgres createuser --superuser tenark
