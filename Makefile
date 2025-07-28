# Makefile para automação de tarefas do AUDITORIA360


install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install uvicorn


run:
	python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	flake8 .

backup-db:
	# Exemplo: pg_dump para Neon (ajuste as variáveis conforme necessário)
	pg_dump "$${DATABASE_URL}" > backup.sql

clean:
	rm -rf __pycache__ .pytest_cache backup.sql

.PHONY: install run test lint backup-db clean
