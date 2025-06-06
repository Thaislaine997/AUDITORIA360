"""
Serviço de monitoramento proativo de fontes oficiais (ex: DOU, Receita Federal).
Busca novas publicações relevantes e aciona o assistente IA de atualização legal.
"""
import requests
import hashlib
import time
import json
from datetime import datetime

# Configurações
DOU_API_URL = "https://servicos.dou.gov.br/api/v2/publicacoes"
PALAVRAS_CHAVE = ["INSS", "IRRF", "FGTS", "salário mínimo", "tabela", "contribuição", "alíquota"]
TIPOS_PARAMETRO = ["INSS", "IRRF", "FGTS", "SALARIO_MINIMO", "SALARIO_FAMILIA"]
ENDPOINT_ANALISAR = "http://localhost:8000/api/v1/parametros/assistente-atualizacao/analisar-documento"
USUARIO_SISTEMA = "monitor_fontes_oficiais"
ARQUIVO_PROCESSADOS = "monitor_fontes_oficiais_processados.json"

# Carrega publicações já processadas
try:
    with open(ARQUIVO_PROCESSADOS, "r", encoding="utf-8") as f:
        processados = set(json.load(f))
except Exception:
    processados = set()

def hash_publicacao(pub):
    return hashlib.sha256((pub["titulo"] + pub.get("identificador", "") + pub.get("dataPublicacao", "")).encode("utf-8")).hexdigest()

def buscar_publicacoes_dou():
    # Exemplo: busca últimas 20 publicações do DOU (ajuste conforme API real)
    params = {"q": " OR ".join(PALAVRAS_CHAVE), "pagina": 1, "itensPorPagina": 20}
    try:
        resp = requests.get(DOU_API_URL, params=params, timeout=20)
        resp.raise_for_status()
        return resp.json().get("publicacoes", [])
    except Exception as e:
        print(f"Erro ao buscar DOU: {e}")
        return []

def filtrar_relevantes(publicacoes):
    relevantes = []
    for pub in publicacoes:
        texto = (pub.get("titulo", "") + " " + pub.get("ementa", "") + " " + pub.get("textoIntegra", "")).lower()
        if any(pal.lower() in texto for pal in PALAVRAS_CHAVE):
            relevantes.append(pub)
    return relevantes

def acionar_assistente(pub):
    texto = pub.get("textoIntegra") or pub.get("ementa") or pub.get("titulo")
    if not texto:
        return False
    tipo_parametro = next((tp for tp in TIPOS_PARAMETRO if tp.lower() in texto.lower()), "OUTRO")
    payload = {
        "tipo_parametro": tipo_parametro,
        "usuario_solicitante": USUARIO_SISTEMA,
        "texto_manual": texto
    }
    try:
        resp = requests.post(ENDPOINT_ANALISAR, data=payload, timeout=60)
        if resp.status_code == 201:
            print(f"Sugestão enviada para publicação: {pub.get('titulo')}")
            return True
        else:
            print(f"Falha ao acionar assistente: {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        print(f"Erro ao acionar assistente: {e}")
        return False

def salvar_processados():
    with open(ARQUIVO_PROCESSADOS, "w", encoding="utf-8") as f:
        json.dump(list(processados), f, ensure_ascii=False, indent=2)

def buscar_publicacoes_receita_federal():
    # Exemplo fictício: simula busca de notícias relevantes na Receita Federal
    # Em produção, use API oficial ou scraping controlado
    url = "https://www.gov.br/receitafederal/pt-br/assuntos/noticias"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            # Busca por palavras-chave no HTML (simples, pode ser melhorado)
            html = resp.text.lower()
            encontrados = []
            for palavra in PALAVRAS_CHAVE:
                if palavra.lower() in html:
                    encontrados.append({
                        "titulo": f"Notícia Receita Federal: {palavra}",
                        "ementa": f"Encontrada menção a '{palavra}' nas notícias da Receita Federal.",
                        "textoIntegra": f"Trecho encontrado: ... ({palavra})",
                        "identificador": f"rf_{palavra}_{datetime.now().isoformat()}",
                        "dataPublicacao": datetime.now().strftime("%Y-%m-%d")
                    })
            return encontrados
        else:
            print(f"[MONITOR] Falha ao buscar Receita Federal: {resp.status_code}")
            return []
    except Exception as e:
        print(f"[MONITOR] Erro ao buscar Receita Federal: {e}")
        return []

def buscar_publicacoes_inss():
    # Exemplo fictício: simula busca de comunicados no INSS
    url = "https://www.gov.br/inss/pt-br/assuntos/noticias"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            html = resp.text.lower()
            encontrados = []
            for palavra in PALAVRAS_CHAVE:
                if palavra.lower() in html:
                    encontrados.append({
                        "titulo": f"Notícia INSS: {palavra}",
                        "ementa": f"Encontrada menção a '{palavra}' nas notícias do INSS.",
                        "textoIntegra": f"Trecho encontrado: ... ({palavra})",
                        "identificador": f"inss_{palavra}_{datetime.now().isoformat()}",
                        "dataPublicacao": datetime.now().strftime("%Y-%m-%d")
                    })
            return encontrados
        else:
            print(f"[MONITOR] Falha ao buscar INSS: {resp.status_code}")
            return []
    except Exception as e:
        print(f"[MONITOR] Erro ao buscar INSS: {e}")
        return []

def main():
    print(f"[MONITOR] Iniciando monitoramento DOU/Receita/INSS em {datetime.now()}")
    publicacoes = buscar_publicacoes_dou()
    publicacoes += buscar_publicacoes_receita_federal()
    publicacoes += buscar_publicacoes_inss()
    relevantes = filtrar_relevantes(publicacoes)
    novos = [pub for pub in relevantes if hash_publicacao(pub) not in processados]
    print(f"[MONITOR] {len(novos)} novas publicações relevantes encontradas.")
    for pub in novos:
        sucesso = acionar_assistente(pub)
        if sucesso:
            processados.add(hash_publicacao(pub))
            salvar_processados()
    print(f"[MONITOR] Monitoramento concluído em {datetime.now()}")

if __name__ == "__main__":
    main()
