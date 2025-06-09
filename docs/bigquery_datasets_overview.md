### **Visão Geral Completa dos Datasets**

---

📁 **1. Dataset: Clientes\_dataset**
* **ID do Conjunto:** `auditoria-folha.Clientes_dataset`
* **Local:** `southamerica-east1`
* **Criado em:** 8 de junho de 2025
* **Tabelas:**
    * 🔹 **Clientes**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_cliente | STRING | REQUIRED |
        | nome\_empresa | STRING | NULLABLE |
        | cnpj | STRING | NULLABLE |
        | data\_criacao | TIMESTAMP | NULLABLE |
        | status | STRING | REQUIRED |
        | configuracoes | JSON | NULLABLE |
    * 🔹 **Papeis**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_papel | STRING | REQUIRED |
        | descricao | STRING | NULLABLE |
    * 🔹 **Usuario\_Papeis**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_usuario | STRING | REQUIRED |
        | id\_papel | STRING | REQUIRED |
    * 🔹 **Usuarios**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_usuario | STRING | REQUIRED |
        | id\_cliente | STRING | NULLABLE |
        | nome | STRING | REQUIRED |
        | email | STRING | REQUIRED |
        | hashed\_password | STRING | REQUIRED |
        | data\_criacao | TIMESTAMP | NULLABLE |
        | ativo | BOOLEAN | REQUIRED |

---

📁 **2. Dataset: Tabelas\_legais\_dataset**
* **ID do Conjunto:** `auditoria-folha.Tabelas_legais_dataset`
* **Local:** `southamerica-east1`
* **Criado em:** 22 de maio de 2025
* **Tabelas:**
    * 🔹 **ConfigFontesOficiaisParametros**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id | STRING | NULLABLE |
        | tipo\_parametro | STRING | NULLABLE |
        | url\_fonte | STRING | NULLABLE |
        | descricao | STRING | NULLABLE |
    * 🔹 **LogVerificacaoManualParametros**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id | STRING | NULLABLE |
        | tipo\_parametro | STRING | NULLABLE |
        | data\_verificacao | DATE | NULLABLE |
        | usuario\_verificacao | STRING | NULLABLE |

---

📁 **3. Dataset: Treinamento**
* **ID do Conjunto:** `auditoria-folha.Treinamento`
* **Local:** `southamerica-east1`
* **Criado em:** 2 de junho de 2025
* **Tabelas:**
    * 🔹 **DatasetTreinamentoRiscosFolha**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_registro | STRING | NULLABLE |
        | id\_folha\_processada\_referencia | STRING | NULLABLE |
        | id\_cliente\_anonimizado | STRING | NULLABLE |
        | periodo\_referencia | STRING | NULLABLE |
        | target\_risco\_ocorrido | BOOLEAN | NULLABLE |
        | severidade\_risco\_ocorrido | STRING | NULLABLE |

---

📁 **4. Dataset: auditoria\_folha\_dataset**
* **ID do Conjunto:** `auditoria-folha.auditoria_folha_dataset`
* **Local:** `southamerica-east1`
* **Tabelas:**
    * (Este dataset contém 13 tabelas detalhadas na resposta anterior, incluindo `CCTsDocumentos`, `ChecklistFechamentoFolha`, `JobsProcessamentoFolha`, etc.)

---

📁 **5. Dataset: controle\_folha\_dataset**
* **ID do Conjunto:** `auditoria-folha.controle_folha_dataset`
* **Local:** `southamerica-east1`
* **Criado em:** 8 de maio de 2025
* **Tabelas:**
    * (Este dataset contém 9 tabelas detalhadas na resposta anterior, incluindo `auditoria_erros`, `empresas`, `folhas`, etc. A tabela `contabilidades` tinha um campo não visível na imagem.)

---

📁 **6. Dataset: controle\_folha\_test\_dataset**
* **ID do Conjunto:** `auditoria-folha.controle_folha_test_dataset`
* **Local:** `southamerica-east1`
* **Criado em:** 9 de maio de 2025
* **Tabelas:**
    * 🔹 **control\_folha\_planilha\_raw\_data**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | cnpj\_empresa | STRING | NULLABLE |
        | status\_valor\_cliente | STRING | NULLABLE |
        | status\_aba\_origem | STRING | NULLABLE |
        | mes\_ano\_referencia | DATE | NULLABLE |
        | data\_processamento\_gcs | TIMESTAMP | NULLABLE |
        | nome\_arquivo\_origem | STRING | NULLABLE |
    * 🔹 **empresas**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | codigo\_empresa | INTEGER | NULLABLE |
        | cnpj | STRING | NULLABLE |
        | nome\_empresa | STRING | NULLABLE |
    * 🔹 **folhas**
        | Campo | Tipo | Modo |
        | :--- | :--- | :--- |
        | id\_folha | STRING | NULLABLE |
        | codigo\_empresa | INTEGER | NULLABLE |
        | cnpj\_empresa | STRING | NULLABLE |
        | mes\_ano | DATE | NULLABLE |
        | status | STRING | NULLABLE |
        | data\_envio\_cliente | TIMESTAMP | NULLABLE |
        | data\_guia\_fgts | TIMESTAMP | NULLABLE |
        | data\_darf\_inss | TIMESTAMP | NULLABLE |
        | observacoes | STRING | NULLABLE |

---
