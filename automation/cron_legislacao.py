import requests
from datetime import date

def buscar_legislacao_diaria():
    url = "https://api.legislacao.gov.br/hoje"
    resp = requests.get(url)
    with open(f"data/updates/{date.today()}.json", "w") as f:
        f.write(resp.text)

if __name__ == "__main__":
    buscar_legislacao_diaria()
