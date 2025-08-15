# Integração IA e Sistema Legado - AUDITORIA360

## 🧠 Visão Geral da Integração de IA

O AUDITORIA360 integra tecnologias de Inteligência Artificial para potencializar os processos de auditoria e compliance trabalhista, mantendo compatibilidade total com sistemas legados existentes.

## 🔗 Arquitetura de Integração

### Sistema Moderno (Next.js)
- **Frontend**: Interface moderna com React 18 + TypeScript
- **Autenticação**: Supabase Auth com proteção de rotas
- **Deploy**: GitHub Actions para deploy automático
- **SEO**: Otimização para motores de busca

### Sistema Legado (Compatibilidade)
- **Frontend**: React/Vite original em `src/frontend/`
- **API**: FastAPI existente em `src/api/`
- **Banco**: Supabase + edge functions
- **Portal**: Sistema de tickets em `portal_demandas/`

## 🤖 Funcionalidades de IA Integradas

### 1. Análise Preditiva de Compliance
- **Localização**: `src/frontend/src/modules/ai/compliance-predictor.ts`
- **Função**: Predição de riscos trabalhistas
- **Integração**: Via Supabase Edge Functions

### 2. Processamento de Documentos
- **Localização**: `supabase/functions/processar-pdf/`
- **Função**: OCR e extração de dados automatizada
- **IA**: Google Gemini API para análise de texto

### 3. Widget ROI Cognitivo
- **Localização**: `src/frontend/src/components/ui/ROICognitivoWidget`
- **Função**: Interface adaptativa baseada em comportamento
- **Tecnologia**: Machine Learning para UX otimizada

### 4. Chatbot Inteligente
- **Localização**: `src/frontend/src/pages/ChatbotPage.tsx`
- **Função**: Suporte automatizado com IA
- **Integração**: API externa + conhecimento da base

## ⚙️ Configuração de IA

### Variáveis de Ambiente Necessárias

```env
# Google AI (Gemini)
GEMINI_API_KEY=your_gemini_api_key

# Supabase (IA/ML)
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# OpenAI (opcional)
OPENAI_API_KEY=your_openai_key
```

### Deployment de Edge Functions

```bash
# Deploy das funções IA
npx supabase functions deploy analisar-texto-com-ia --no-verify-jwt
npx supabase functions deploy processar-pdf --no-verify-jwt
```

## 🔄 Fluxo de Migração IA

### Fase 1: Compatibilidade (✅ Concluída)
- [x] Manter funcionalidades IA existentes no legado
- [x] Integrar autenticação Supabase no sistema moderno
- [x] Deploy automatizado funcionando

### Fase 2: Unificação (🔄 Em Progresso)
- [x] Migrar páginas principais para Next.js
- [ ] Integrar widgets IA no dashboard moderno
- [ ] Unificar APIs de IA

### Fase 3: Otimização (⏳ Planejada)
- [ ] Melhorar performance das predições
- [ ] Implementar cache inteligente
- [ ] Otimizar modelos de ML

## 📊 Métricas de IA Monitoradas

1. **Precisão de Predições**: 87% (meta: >90%)
2. **Tempo de Processamento**: 2.3s (meta: <2s)
3. **Taxa de Automação**: 65% (meta: >70%)
4. **Satisfação do Usuário**: 4.2/5 (meta: >4.5)

## 🛠️ APIs de IA Disponíveis

### Análise de Texto
```typescript
POST /api/ai/analyze-text
{
  "text": "documento texto",
  "type": "compliance|legal|financial"
}
```

### Predição de Riscos
```typescript
POST /api/ai/predict-risks
{
  "company_data": {...},
  "period": "monthly|quarterly|annual"
}
```

### Processamento de PDF
```typescript
POST /api/ai/process-pdf
Content-Type: multipart/form-data
{
  "file": pdf_file,
  "extract_type": "parameters|full_text|structured"
}
```

## 🔒 Segurança e Compliance IA

- **LGPD**: Todos os dados processados seguem diretrizes LGPD
- **Auditoria**: Logs completos de todas as operações IA
- **Backup**: Sistema automatizado de backup via Cloudflare Workers
- **Monitoramento**: Health checks contínuos das APIs IA

## 📚 Documentação Técnica

- **Supabase Functions**: `supabase/README.md`
- **APIs Legacy**: `src/api/README.md`
- **Frontend Components**: Inline documentation
- **Edge Functions**: JSDoc completa

---

**Desenvolvido com ❤️ usando Next.js + Supabase + IA**