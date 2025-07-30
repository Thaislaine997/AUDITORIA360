# 🔐 Configurações de Autenticação - AUDITORIA360

Este diretório contém as configurações de autenticação para o sistema AUDITORIA360.

## 📁 Arquivos

### Arquivos de Template (Versionados)
- `login.example.yaml` - Template para configuração de login com Streamlit Authenticator
- `gestor_contas.example.json` - Template para contas de gestores e administradores

### Arquivos de Produção (NÃO Versionados)
- `login.yaml` - Configuração real de login (criado a partir do template)
- `gestor_contas.json` - Contas reais de usuários (criado a partir do template)

## 🚀 Como Configurar

### 1. Configuração Inicial
```bash
# Copie os templates para os arquivos de produção
cp auth/login.example.yaml auth/login.yaml
cp auth/gestor_contas.example.json auth/gestor_contas.json
```

### 2. Configurar Credenciais
Edite os arquivos copiados e substitua:

#### Em `login.yaml`:
- Substitua `REPLACE_WITH_STRONG_RANDOM_KEY_MINIMUM_32_CHARACTERS` por uma chave forte
- Substitua `$2b$12$EXAMPLE_HASH_REPLACE_WITH_REAL_BCRYPT_HASH` por hashes bcrypt reais
- Atualize emails e nomes de usuários

#### Em `gestor_contas.json`:
- Substitua os hashes de exemplo por hashes bcrypt reais
- Atualize usernames e client_ids conforme necessário

### 3. Gerar Hashes de Senha
Use o script utilitário para gerar hashes bcrypt:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash_senha = pwd_context.hash("sua_senha_aqui")
print(hash_senha)
```

### 4. Gerar Chave Secreta
```python
import secrets
secret_key = secrets.token_urlsafe(32)
print(secret_key)
```

## ⚠️ Segurança

- **NUNCA** commite os arquivos de produção (`login.yaml`, `gestor_contas.json`)
- Estes arquivos estão no `.gitignore` para sua proteção
- Use senhas fortes e únicas para cada ambiente
- Rotacione chaves secretas regularmente
- Em produção, considere usar AWS Secrets Manager ou similar

## 🔍 Validação

Execute o script de validação de segurança:
```bash
python scripts/security_validation.py
```

## 📚 Documentação

Para mais informações sobre autenticação, consulte:
- `/docs/security.md`
- `/docs/authentication.md`