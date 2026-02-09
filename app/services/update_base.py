import requests
import json
import os

from ..config import(
    URL_GREAT,
    URL_ULTRA,
    URL_MASTER
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def update_json(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        path = os.path.join(DATA_DIR, filename)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Sucesso: {filename} atualizado em {path}")

    except Exception as e:
        print(f"Erro ao atualizar {filename}: {e}")

update_json(URL_GREAT, 'base_great.json')
update_json(URL_ULTRA, 'base_ultra.json')
update_json(URL_MASTER, 'base_master.json')