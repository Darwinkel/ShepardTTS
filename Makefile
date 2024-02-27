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
