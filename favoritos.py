import json
from pathlib import Path

FAV_FILE = Path("favoritos.json")
HIST_FILE = Path("historico.json")

def salvar_favorito(url, titulo=None):
    favoritos = carregar_favoritos()
    favoritos.append({"url": url, "titulo": titulo or url})
    with open(FAV_FILE, "w") as f:
        json.dump(favoritos, f)

def carregar_favoritos():
    if FAV_FILE.exists():
        return json.load(open(FAV_FILE))
    return []

def salvar_historico(url):
    historico = carregar_historico()
    historico.append(url)
    with open(HIST_FILE, "w") as f:
        json.dump(historico, f)

def carregar_historico():
    if HIST_FILE.exists():
        return json.load(open(HIST_FILE))
    return []