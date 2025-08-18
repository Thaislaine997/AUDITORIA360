# Checklist de Migração AUDITORIA360

## Status Geral da Migração

- [x] ✅ Estrutura Next.js base implementada
- [x] ✅ Configuração de build corrigida
- [x] ✅ Páginas principais migradas (Home, Login, Dashboard)
- [x] ✅ Supabase integrado e funcionando
- [ ] 🔄 Inventário completo do sistema legado
- [ ] 🔄 Migração sistemática de componentes
- [ ] 🔄 Limpeza de arquivos obsoletos

## Arquivos Base Migrados (✅ Concluído)

- [x] `/pages/_app.tsx` - App wrapper principal
- [x] `/pages/index.tsx` - Homepage institucional
- [x] `/pages/login.tsx` - Página de autenticação
- [x] `/pages/dashboard.tsx` - Dashboard protegido
- [x] `/components/layout/Layout.tsx` - Layout principal
- [x] `/lib/supabaseClient.ts` - Cliente Supabase
- [x] `/styles/globals.css` - Estilos globais

## Sistema Legado Identificado (📊 Total: 212 arquivos TS/TSX)

### Páginas Legadas para Migração

```
./src/frontend/src/pages/
├── SindicatoDetailPage.tsx
├── RelatorioDetailPage.tsx
├── Dashboard.tsx
├── GestaoLegislacaoPage.tsx
├── GestaoClientes.tsx
├── UploadDetailPage.tsx
├── TicketDetailPage.tsx
├── CCTDetailPage.tsx
├── TarefaDetailPage.tsx
├── PortalDemandasDashboard.tsx
├── ControleMensalPage.tsx
├── AuditoriaDetailPage.tsx
├── ValidacaoIAPage.tsx
├── EmpresaDetailPage.tsx
└── ... (mais páginas)
```

## Próximos Passos da Migração

1. **Inventário Completo**: Catalogar todos os 212 arquivos por categoria
2. **Migração por Prioridade**: Começar com funcionalidades core
3. **Validação**: Testar cada migração antes de remover legado
4. **Limpeza**: Remover arquivos obsoletos após validação

## Diretrizes de Migração

- ✅ **Migrar antes de excluir**
- ✅ **Validar cada rota e funcionalidade**
- ✅ **Documentar cada alteração**
- ✅ **Manter código limpo e tipado**
- ✅ **Seguir padrões Next.js**
