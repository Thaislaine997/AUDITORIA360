# 📚 AUDITORIA360 - Documentação Fonte

> **Fonte única da verdade para toda documentação do projeto AUDITORIA360**

Esta é a **única localização** onde a documentação deve ser editada. Todo conteúdo aqui é automaticamente sincronizado com a Wiki do GitHub através do workflow de automação.

## 📋 Estrutura da Documentação

```
docs-source/
├── README.md                           # Este arquivo
├── Home.md                            # Página inicial da Wiki
├── user-manuals/                      # 👤 Manuais do Usuário
│   ├── getting-started.md
│   ├── user-guide.md
│   └── faq.md
├── developer-guides/                  # 👨‍💻 Guias para Desenvolvedores
│   ├── development-setup.md
│   ├── api-documentation.md
│   ├── architecture-overview.md
│   └── contributing.md
├── architecture-decisions/            # 🏗️ Decisões de Arquitetura (ADRs)
│   ├── README.md
│   └── adr-template.md
├── api-reference/                     # 📡 Referência da API
│   ├── README.md
│   ├── authentication.md
│   └── endpoints/
└── strategic/                         # 📊 Documentação Estratégica
    ├── project-status.md
    ├── roadmap.md
    └── performance-metrics.md
```

## ⚠️ Processo Obrigatório

**IMPORTANTE**: A partir desta implementação, toda Pull Request que modificar funcionalidades DEVE incluir atualizações na documentação correspondente neste diretório.

## 🔄 Sincronização Automática

- Modificações neste diretório são automaticamente sincronizadas com a Wiki
- O workflow `sync-wiki.yml` é executado a cada push na branch `main`
- A documentação pública estará sempre atualizada com a versão estável do código

## 📖 Como Usar

1. **Editar**: Faça suas alterações nos arquivos deste diretório
2. **Commit**: Inclua as mudanças na sua PR
3. **Merge**: Após merge na main, a Wiki é atualizada automaticamente