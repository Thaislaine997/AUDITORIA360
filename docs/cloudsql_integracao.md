# Guia Completo de Integração Cloud SQL PostgreSQL no AUDITORIA360

## 1. Dados de Conexão

```
DATABASE_URL=postgresql+psycopg2://datastream_user:41283407@10.128.0.4:5432/auditoria_db
CLOUD_SQL_INSTANCE=auditoria-folha:us-central1:auditoria360portal
CLOUD_SQL_INTERNAL_IP=10.128.0.4
CLOUD_SQL_EXTERNAL_IP=34.122.122.122
CLOUD_SQL_DB_NAME=auditoria_db
CLOUD_SQL_DB_USER=datastream_user
CLOUD_SQL_DB_PASSWORD=41283407
CLOUD_SQL_DB_PORT=5432
SERVICE_ACCOUNT=333253866645-compute@developer.gserviceaccount.com
```

## 2. Usos e Integrações

- **Backend/API:** Armazenamento e consulta de dados, autenticação, auditorias, logs, integrações, relatórios.
- **Dashboards:** KPIs, gráficos, checklist, trilha de auditoria, benchmarking em tempo real.
- **Datastream para BigQuery:** Sincronização automática para análises avançadas, BI, Data Studio, ML.
- **ETL/ELT:** Pipelines Python, Airflow, Dataflow para movimentação e transformação de dados.
- **Automação/Robôs:** Registro de resultados, status e logs de automações e integrações.
- **Auditoria e Compliance:** Trilhas de auditoria, logs de acesso, alterações e conformidade.
- **Backup e Recuperação:** Backups automáticos, snapshots e recuperação pontual.
- **Multi-ambiente:** Produção, homologação e desenvolvimento com bancos separados.
- **Acesso seguro:** IP privado, VPC, Service Account, firewall.
- **Integração Google Cloud:** BigQuery, Dataflow, Vertex AI, Cloud Functions.

## 3. Exemplos Práticos

### Python (SQLAlchemy)
```python
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
conn = engine.connect()
print(conn.execute('SELECT 1'))
```

### Docker
```dockerfile
# Dockerfile
ENV DATABASE_URL=postgresql+psycopg2://datastream_user:41283407@10.128.0.4:5432/auditoria_db
```

### Cloud Run
- Adicione as variáveis do `.env.cloudsql` nas configurações do serviço.
- Configure a conexão ao Cloud SQL com o nome da instância.

### Datastream
- Origem: perfil `auditoria360portal` (PostgreSQL)
- Destino: perfil `auditoria360` (BigQuery)
- Inclui todas as tabelas e esquemas
- Modo de gravação: Mesclar

## 4. Segurança
- Use IP privado e Service Account.
- Proteja variáveis sensíveis com Secret Manager.
- Restrinja acesso via firewall.
- Nunca exponha senhas em repositórios públicos.

## 5. Checklist de Deploy
- [x] Instância Cloud SQL criada
- [x] Banco e usuário configurados
- [x] Variáveis de ambiente definidas
- [x] Firewall e rede ajustados
- [x] Service Account vinculada
- [x] Teste de conexão realizado
- [x] Datastream configurado para BigQuery

---
Este documento serve como referência única para integração, automação e segurança do banco Cloud SQL no AUDITORIA360.
