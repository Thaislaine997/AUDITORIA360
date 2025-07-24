import requests

def checar_servico(nome, url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            print(f"{nome}: OK")
        else:
            print(f"{nome}: Falha ({resp.status_code})")
    except Exception as e:
        print(f"{nome}: Erro ({e})")

servicos = {
    "API Demandas": "http://localhost:8000/api/demandas",
    "API Folha": "http://localhost:8000/api/folha",
}

for nome, url in servicos.items():
    checar_servico(nome, url)
