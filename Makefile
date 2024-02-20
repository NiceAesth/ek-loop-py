run:
	poetry run python main.py

shell:
	poetry shell

lint:
	poetry run pre-commit run --all-files

install:
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install --no-root

install-dev:
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install --no-root --with dev
	poetry run pre-commit install

uninstall:
	poetry env remove python

release:
	poetry version $(ver)
