# Onboarding Dev (15 minutos)

1. Pré-requisitos
   - Python 3.11+, Node 18+, Docker
2. Clone o repo
   ```bash
   git clone git@github.com:Thaislaine997/AUDITORIA360.git
   cd AUDITORIA360
   ```
3. Backend (venv)
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # criar DB local
   export DATABASE_URL=postgres://postgres:postgres@localhost:5432/auditoria_dev
   python setup_database.py --db-url "$DATABASE_URL"
   # rodar
   uvicorn api.index:app --reload
   ```
4. Frontend
   ```bash
   cd frontend
   npm ci
   npm run dev
   ```
5. Rodar testes
   ```bash
   # backend
   pytest -q
   # e2e (frontend)
   npx playwright test
   ```
6. Troubleshooting rápido
   - Erro de DB: verifique variáveis de ambiente e se Postgres está rodando
   - Erro de dependências: delete virtualenv/ node_modules e reinstale

7. Contatos/FAQs
   - Canal Slack: #auditoria360
   - Responsável infra: @ops
