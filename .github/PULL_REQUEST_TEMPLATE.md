## ✅ Checklist para Pull Request: Integração do Servidor MCP Local

### 🧪 Testes Locais

- [ ] O servidor MCP local foi iniciado com sucesso utilizando o comando configurado (ex: `npm start`)?
- [ ] O servidor responde corretamente em `http://localhost:3000` (ou outra porta configurada)?

### 🔧 Configuração do Servidor MCP no GitHub

- [ ] A configuração do servidor MCP foi adicionada corretamente no repositório GitHub?
  - **Settings → Code & automation → Copilot → Coding agent → MCP configuration**
  - Formato JSON válido
  - Exemplo:

    ```json
    {
      "mcpServers": {
        "localMCP": {
          "type": "local",
          "command": "npm",
          "args": ["start"],
          "tools": ["*"]
        }
      }
    }
    ```

### 🧪 Testes de Integração com o Copilot

- [ ] Uma nova issue foi criada e atribuída ao Copilot?
- [ ] O Copilot iniciou automaticamente o servidor MCP local?
- [ ] O Copilot utilizou as ferramentas definidas no servidor MCP para interagir com o repositório?

### 📄 Documentação e Comunicação

- [ ] A descrição do PR inclui informações claras sobre a configuração do servidor MCP e sua integração com o Copilot?
- [ ] Foram adicionados comentários no código explicando a configuração do servidor MCP e sua finalidade?

### 🔐 Segurança e Boas Práticas

- [ ] A configuração do servidor MCP expõe apenas ferramentas seguras e necessárias?
- [ ] Não há informações sensíveis (como senhas ou tokens) expostas na configuração do servidor MCP?

### 📋 Checklist Adicional AUDITORIA360

- [ ] Meu código segue as convenções do projeto
- [ ] Realizei self-review do código
- [ ] Testes unitários e integração passam localmente
- [ ] RLS (Row Level Security) foi considerado para isolamento multi-tenant
- [ ] Não há vazamento de secrets nos logs ou código
- [ ] Atualizei a documentação (se aplicável)
