# ⚠️ DEPRECATED - Legacy API Structure

**Esta pasta `api/` está marcada como DEPRECATED desde a Grande Síntese (Agosto 2025).**

## 🚨 Aviso Importante

Todo novo desenvolvimento de API deve ser feito na estrutura moderna em `src/api/`.

### Motivos da Depreciação:

1. **Arquitetura Obsoleta**: Estrutura não suporta as melhas práticas modernas
2. **Falta de Instrumentação**: Sem suporte ao ACR (Agente de Rastreamento Cinético)
3. **Monitoramento Limitado**: Sem integração com ACH (Agente de Consciência Holística)
4. **Escalabilidade**: Não preparada para crescimento do sistema

### 📍 Nova Localização:

```
src/api/          <- ✅ USE ESTA ESTRUTURA
├── routers/      <- Routers organizados por domínio  
├── common/       <- Middleware e utilitários
└── ...
```

### 🔄 Migração:

Para migrar código desta pasta:

1. Mova os arquivos para `src/api/`
2. Atualize as importações
3. Adicione instrumentação OpenTelemetry
4. Teste com ACR e ACH

### ⏰ Timeline de Remoção:

- **Fase 1** (atual): Marcação como deprecated
- **Fase 2** (Q1 2026): Adição de warnings em runtime
- **Fase 3** (Q2 2026): Remoção completa

---

**Grande Síntese - Initiative IV: Strategic Implementation**