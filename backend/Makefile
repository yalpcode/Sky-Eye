PYTHON_VERSION := 3.12
POETRY := $(shell command -v poetry 2> /dev/null)
INSTALL_STAMP := .install.stamp


.PHONY: run
uvicorn: install
	poetry run uvicorn --reload --log-level=info --workers 2 --host 0.0.0.0 --port 8000 src.main:app


install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	$(POETRY) run pip install --upgrade pip setuptools
	poetry install
	touch $(INSTALL_STAMP)
