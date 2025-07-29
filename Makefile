# Makefile para automação de tarefas do AUDITORIA360


install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install uvicorn

install-dev:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install uvicorn black isort flake8 autoflake pre-commit

run:
	python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8000

test:
	pytest

# Code quality commands
format:
	black .
	isort .
	autoflake --in-place --remove-all-unused-imports --recursive .

lint:
	flake8 .

check:
	black --check .
	isort --check-only .
	flake8 .

quality: format lint
	@echo "✅ Code quality checks completed"

# Database and cleanup
backup-db:
	# Exemplo: pg_dump para Neon (ajuste as variáveis conforme necessário)
	pg_dump "$${DATABASE_URL}" > backup.sql

clean:
	rm -rf __pycache__ .pytest_cache backup.sql
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Pre-commit setup
setup-hooks:
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

.PHONY: install install-dev run test format lint check quality backup-db clean setup-hooks
