### **Visão Geral Completa dos Datasets**

---

📁 **1. Dataset: Clientes_dataset**

- **ID do Conjunto:** `auditoria-folha.Clientes_dataset`
- **Local:** `southamerica-east1`
- **Criado em:** 8 de junho de 2025
- **Tabelas:**
  - 🔹 **Clientes**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_cliente | STRING | REQUIRED |
    | nome_empresa | STRING | NULLABLE |
    | cnpj | STRING | NULLABLE |
    | data_criacao | TIMESTAMP | NULLABLE |
    | status | STRING | REQUIRED |
    | configuracoes | JSON | NULLABLE |
  - 🔹 **Papeis**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_papel | STRING | REQUIRED |
    | descricao | STRING | NULLABLE |
  - 🔹 **Usuario_Papeis**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_usuario | STRING | REQUIRED |
    | id_papel | STRING | REQUIRED |
  - 🔹 **Usuarios**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_usuario | STRING | REQUIRED |
    | id_cliente | STRING | NULLABLE |
    | nome | STRING | REQUIRED |
    | email | STRING | REQUIRED |
    | hashed_password | STRING | REQUIRED |
    | data_criacao | TIMESTAMP | NULLABLE |
    | ativo | BOOLEAN | REQUIRED |

---

📁 **2. Dataset: Tabelas_legais_dataset**

- **ID do Conjunto:** `auditoria-folha.Tabelas_legais_dataset`
- **Local:** `southamerica-east1`
- **Criado em:** 22 de maio de 2025
- **Tabelas:**
  - 🔹 **ConfigFontesOficiaisParametros**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id | STRING | NULLABLE |
    | tipo_parametro | STRING | NULLABLE |
    | url_fonte | STRING | NULLABLE |
    | descricao | STRING | NULLABLE |
  - 🔹 **LogVerificacaoManualParametros**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id | STRING | NULLABLE |
    | tipo_parametro | STRING | NULLABLE |
    | data_verificacao | DATE | NULLABLE |
    | usuario_verificacao | STRING | NULLABLE |

---

📁 **3. Dataset: Treinamento**

- **ID do Conjunto:** `auditoria-folha.Treinamento`
- **Local:** `southamerica-east1`
- **Criado em:** 2 de junho de 2025
- **Tabelas:**
  - 🔹 **DatasetTreinamentoRiscosFolha**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_registro | STRING | NULLABLE |
    | id_folha_processada_referencia | STRING | NULLABLE |
    | id_cliente_anonimizado | STRING | NULLABLE |
    | periodo_referencia | STRING | NULLABLE |
    | target_risco_ocorrido | BOOLEAN | NULLABLE |
    | severidade_risco_ocorrido | STRING | NULLABLE |

---

📁 **4. Dataset: auditoria_folha_dataset**

- **ID do Conjunto:** `auditoria-folha.auditoria_folha_dataset`
- **Local:** `southamerica-east1`
- **Tabelas:**
  - (Este dataset contém 13 tabelas detalhadas na resposta anterior, incluindo `CCTsDocumentos`, `ChecklistFechamentoFolha`, `JobsProcessamentoFolha`, etc.)

---

📁 **5. Dataset: controle_folha_dataset**

- **ID do Conjunto:** `auditoria-folha.controle_folha_dataset`
- **Local:** `southamerica-east1`
- **Criado em:** 8 de maio de 2025
- **Tabelas:**
  - (Este dataset contém 9 tabelas detalhadas na resposta anterior, incluindo `auditoria_erros`, `empresas`, `folhas`, etc. A tabela `contabilidades` tinha um campo não visível na imagem.)

---

📁 **6. Dataset: controle_folha_test_dataset**

- **ID do Conjunto:** `auditoria-folha.controle_folha_test_dataset`
- **Local:** `southamerica-east1`
- **Criado em:** 9 de maio de 2025
- **Tabelas:**
  - 🔹 **control_folha_planilha_raw_data**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | cnpj_empresa | STRING | NULLABLE |
    | status_valor_cliente | STRING | NULLABLE |
    | status_aba_origem | STRING | NULLABLE |
    | mes_ano_referencia | DATE | NULLABLE |
    | data_processamento_gcs | TIMESTAMP | NULLABLE |
    | nome_arquivo_origem | STRING | NULLABLE |
  - 🔹 **empresas**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | codigo_empresa | INTEGER | NULLABLE |
    | cnpj | STRING | NULLABLE |
    | nome_empresa | STRING | NULLABLE |
  - 🔹 **folhas**
    | Campo | Tipo | Modo |
    | :--- | :--- | :--- |
    | id_folha | STRING | NULLABLE |
    | codigo_empresa | INTEGER | NULLABLE |
    | cnpj_empresa | STRING | NULLABLE |
    | mes_ano | DATE | NULLABLE |
    | status | STRING | NULLABLE |
    | data_envio_cliente | TIMESTAMP | NULLABLE |
    | data_guia_fgts | TIMESTAMP | NULLABLE |
    | data_darf_inss | TIMESTAMP | NULLABLE |
    | observacoes | STRING | NULLABLE |

---
