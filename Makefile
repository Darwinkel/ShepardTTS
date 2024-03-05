format:
	ruff format shepardtts

check:
	ruff check shepardtts

typing:
	mypy shepardtts/*.py

quality:
	make format
	make check
	make typing

build:
	poetry build -f wheel

test:
	poetry run pytest --doctest-modules --junitxml=junit/test-results.xml --cov=shepardtts --cov-report=xml --cov-report=html tests
