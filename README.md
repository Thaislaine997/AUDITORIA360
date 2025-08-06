# AUDITORIA360

# AUDITORIA360

Documentação principal agora está disponível no [Wiki do projeto](../../wiki).
- Para históricos, migrações e detalhes técnicos, veja a pasta [`/docs`](./docs).
- Exemplos, scripts e testes estão organizados em `/demos`, `/scripts` e `/tests`.

## Comece aqui

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Veja [Como rodar](../../wiki/Como-rodar) no Wiki.

## Contribuições e dúvidas
- Leia as [regras de contribuição](../../wiki/Contribuindo).
- Dúvidas? Abra uma issue ou consulte o Wiki.

---

## Estrutura do Projeto

```plaintext
/
├── src/                  # Código-fonte principal
├── services/             # Serviços de ML, ingestão, componentes
├── demos/                # Scripts de demonstração e relatórios
├── tests/                # Testes automatizados
├── scripts/              # Scripts de automação e utilitários
├── web/                  # Arquivos HTML e dashboards
├── conf/                 # Configurações de webserver
├── docs/                 # Documentação técnica e histórica
└── requirements*.txt     # Dependências do projeto
```

Para automatizar a reorganização da estrutura, use:
```bash
./scripts/reorganizar_estrutura.sh
```