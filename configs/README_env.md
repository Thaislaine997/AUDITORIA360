# Como usar variáveis de ambiente no AUDITORIA360

- Sempre use o arquivo `.env.example` como referência para criar seu `.env` local.
- Nunca faça commit do `.env` real.
- Todas as variáveis sensíveis devem ser cadastradas no painel da Vercel em "Environment Variables".
- Para rodar localmente, copie `.env.example` para `.env` e preencha com seus segredos.

## Variáveis obrigatórias

- DATABASE_URL
- CLOUDFLARE_ACCOUNT_ID
- R2_BUCKET_NAME
- R2_ACCESS_KEY_ID
- R2_SECRET_ACCESS_KEY
- SECRET_KEY
- ALGORITHM

Consulte sempre o plano e o README principal para detalhes atualizados.
