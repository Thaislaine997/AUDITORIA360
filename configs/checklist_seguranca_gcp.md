# Checklist de Segurança GCP para o projeto AUDITORIA360

1. **Configurações e Credenciais**
   - [x] Todos os arquivos de configuração sensível (.json, .yaml, .key) estão protegidos por criptografia ou fora do versionamento público.
   - [x] O arquivo `.gitignore` está reforçado para evitar vazamento de configs e backups.
   - [ ] Variáveis de ambiente são usadas para credenciais e project_id em produção.

2. **Código Fonte**
   - [x] Referências a project_id, service_account, IAM, policy, bigquery, documentai e cloud_storage estão centralizadas em arquivos protegidos.
   - [ ] Nenhum dado sensível é exposto em logs, erros ou documentação pública.

3. **Auditoria e Monitoramento**
   - [ ] Auditoria periódica dos arquivos do projeto para novas referências a dados GCP.
   - [ ] Revisão de permissões IAM e políticas no arquivo `gcp_resources_iam_policies_private.json`.

4. **Execução de Scripts de Segurança**
   - [ ] O script de criptografia foi executado com sucesso e todos os arquivos sensíveis estão protegidos.
   - [ ] O ambiente Python está configurado corretamente para rodar scripts de segurança.

5. **Backup e Recuperação**
   - [ ] Backups criptografados e fora do versionamento público.
   - [ ] Procedimento de recuperação/descriptografia documentado.

---

> **Atenção:** Nunca compartilhe senhas, chaves ou arquivos protegidos fora do ambiente seguro. Sempre revise permissões e mantenha o checklist atualizado.
