# Orquestração Inteligente: Vertex AI + Gemini

## Objetivo

- **Vertex AI (Tradicional):** Classificação de alta precisão de rubricas trabalhistas (endpoint customizado).
- **Gemini (Generativo):** Geração de explicações, descrições e compreensão de linguagem natural.

---

## 1. vertex_utils.py – Classificação Precisa de Rubricas

- Função principal: `prever_rubrica_com_vertex(texto_clausula: str)`
- Use para obter a rubrica mais confiável possível.
- Melhore logs e tratamento de erro se necessário.

**Exemplo de uso:**

```python
rubrica = prever_rubrica_com_vertex("Texto da cláusula trabalhista...")
```

---

## 2. gemini_utils.py – Geração de Texto e Explicações

- Função principal: `gerar_descricao_da_clausula_com_gemini(texto_clausula, rubrica_identificada=None)`
- Use para gerar explicações detalhadas, com ou sem rubrica já identificada.
- Função auxiliar: `_extrair_json_de_texto(texto: str)` para robustez na extração do JSON da resposta do Gemini.

**Exemplo de uso:**

```python
descricao = gerar_descricao_da_clausula_com_gemini("Texto da cláusula", rubrica_identificada=rubrica)
```

---

## 3. Fluxo Sugerido de Orquestração

```python
def analisar_clausula_completa(texto_da_clausula: str) -> dict:
    resultado_analise = {
        "clausula": texto_da_clausula,
        "rubrica_vertex_ai": None,
        "descricao_gemini": None,
        "erros": []
    }
    # 1. Classificar com Vertex AI
    try:
        rubrica_vertex = prever_rubrica_com_vertex(texto_da_clausula)
        if "Erro" in rubrica_vertex:
            resultado_analise["erros"].append(f"Vertex AI: {rubrica_vertex}")
        else:
            resultado_analise["rubrica_vertex_ai"] = rubrica_vertex
    except Exception as e:
        resultado_analise["erros"].append(f"Exceção ao chamar Vertex AI: {str(e)}")
    # 2. Gerar descrição com Gemini
    try:
        rubrica_para_gemini = resultado_analise["rubrica_vertex_ai"] if resultado_analise["rubrica_vertex_ai"] and "Erro" not in resultado_analise["rubrica_vertex_ai"] else None
        info_gemini = gerar_descricao_da_clausula_com_gemini(
            texto_clausula=texto_da_clausula,
            rubrica_identificada=rubrica_para_gemini
        )
        if "erro" in info_gemini:
            resultado_analise["erros"].append(f"Gemini: {info_gemini['erro']}")
        elif "descricao" in info_gemini:
            resultado_analise["descricao_gemini"] = info_gemini["descricao"]
            if "rubrica" in info_gemini and not rubrica_para_gemini:
                resultado_analise["rubrica_gemini_sugerida"] = info_gemini["rubrica"]
        else:
            resultado_analise["erros"].append("Gemini: Descrição não retornada ou formato inesperado.")
    except Exception as e:
        resultado_analise["erros"].append(f"Exceção ao chamar Gemini: {str(e)}")
    return resultado_analise
```

---

## 4. Benefícios

- Vertex AI: máxima precisão na classificação.
- Gemini: explicações ricas e adaptáveis.
- Flexibilidade para fallback e comparação.

---

## 5. Checklist de Implementação

- [ ] `vertex_utils.py`: endpoint configurado, função robusta, logging.
- [ ] `gemini_utils.py`: função de geração de descrição, extração de JSON robusta.
- [ ] Orquestração implementada no controller ou serviço.
- [ ] Testes com cláusulas reais.

---

**Dica:** Consulte sempre a documentação dos endpoints e ajuste as chaves de resposta conforme o seu modelo.
