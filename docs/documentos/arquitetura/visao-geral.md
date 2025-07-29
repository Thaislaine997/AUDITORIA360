# Visão Geral da Arquitetura - AUDITORIA360

> **Redirecionamento para documentação técnica principal**

Este documento foi movido para manter a organização da estrutura de documentos.

📍 **Localização atual:** [`../../tecnico/arquitetura/`](../../tecnico/arquitetura/)

## Acesso Direto

Para acessar a documentação de arquitetura completa, navegue para:

- 🏗️ **Arquitetura Geral**: [`../../tecnico/arquitetura/`](../../tecnico/arquitetura/)
- 🔧 **Módulos Principais**: [`../../tecnico/modulos-principais.md`](../../tecnico/modulos-principais.md)
- 💾 **Banco de Dados**: [`../../tecnico/banco-dados/`](../../tecnico/banco-dados/)
- 🚀 **Deploy**: [`../../tecnico/deploy/`](../../tecnico/deploy/)

## Componentes Principais

O sistema AUDITORIA360 é baseado em arquitetura serverless com:

### Stack Tecnológica

- **Frontend**: React.js + TypeScript + Material UI
- **Backend**: FastAPI (Python)
- **Banco de Dados**: Neon (PostgreSQL serverless)
- **Armazenamento**: Cloudflare R2
- **Analytics**: DuckDB (embedded)
- **OCR**: PaddleOCR
- **IA**: OpenAI GPT Integration
- **Deploy**: Vercel + GitHub Actions

### Segurança e Compliance

- **Autenticação**: OAuth2 + JWT
- **Criptografia**: Dados sensíveis criptografados
- **LGPD**: Consentimento explícito e anonimização
- **Backup**: Automatizado para Neon e R2
- **Firewall**: Cloudflare (DDoS protection)

---

**Mantido sincronizado com a estrutura principal de documentação**
