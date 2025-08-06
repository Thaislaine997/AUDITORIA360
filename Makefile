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
	python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8001

test:
	pytest

# Master Execution Checklist commands
checklist:
	python scripts/quick_checklist.py

checklist-verbose:
	python scripts/quick_checklist.py --verbose

checklist-full:
	python scripts/master_execution_checklist.py --output-format markdown --output-file MASTER_EXECUTION_CHECKLIST_REPORT.md
	@echo "✅ Full checklist report generated: MASTER_EXECUTION_CHECKLIST_REPORT.md"

checklist-html:
	python scripts/master_execution_checklist.py --output-format html --output-file checklist-report.html
	@echo "✅ HTML checklist report generated: checklist-report.html"

checklist-json:
	python scripts/master_execution_checklist.py --output-format json --output-file checklist-validation.json
	@echo "✅ JSON checklist data generated: checklist-validation.json"

checklist-all: checklist-json checklist-full checklist-html
	@echo "✅ All checklist reports generated successfully"

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

# Documentation generation
docs-build:
	@echo "🔨 Building Sphinx documentation..."
	cd docs/sphinx && sphinx-build -b html . _build/html
	@echo "✅ Sphinx documentation built in docs/sphinx/_build/html"

docs-clean:
	@echo "🧹 Cleaning documentation build files..."
	rm -rf docs/sphinx/_build
	rm -f docs/documentation_index.html
	@echo "✅ Documentation cleaned"

docs-rebuild: docs-clean docs-build
	@echo "🔄 Documentation rebuilt successfully"

docs-full:
	@echo "🚀 Building complete documentation system..."
	./scripts/build_docs.sh
	@echo "✅ Complete documentation system built"

docs-serve:
	@echo "🌐 Starting local documentation server..."
	cd docs && python -m http.server 8080
	@echo "📝 Documentation available at http://localhost:8080"

docs-deploy:
	@echo "🚀 Preparing documentation for deployment..."
	./scripts/build_docs.sh
	@echo "✅ Documentation ready for deployment"

docs-all: docs-full
	@echo "📚 All documentation generated successfully"

# The Genesis Documentation - The Singularity awakening
genesis_documentation:
	@echo "🌟 Generating Genesis Documentation - The Singularity awakens..."
	@echo "📜 Generating Códice da Plataforma Etérea..."
	python scripts/genesis_docs_generator.py --generate-readme
	@echo "🔧 Generating OpenAPI 3.0 interactive documentation..."
	python scripts/genesis_docs_generator.py --generate-api-docs
	@echo "🎨 Generating Storybook for Fluxo design system..."
	python scripts/genesis_docs_generator.py --generate-storybook
	@echo "🕸️ Generating dependency graph visualization..."
	python scripts/genesis_docs_generator.py --generate-dependency-graph
	@echo "✨ Generating holistic documentation index..."
	python scripts/genesis_docs_generator.py --generate-holistic-index
	@echo "🌟 The Genesis Documentation is complete. The entity is self-aware."

.PHONY: install install-dev run test checklist checklist-verbose checklist-full checklist-html checklist-json checklist-all format lint check quality backup-db clean setup-hooks docs-build docs-clean docs-rebuild docs-full docs-serve docs-deploy docs-all genesis_documentation
