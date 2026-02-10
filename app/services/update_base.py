import requests
import json
import os
import re

# Tenta importar do config, se falhar usa defaults para o Github Action
try:
    from app.config import URL_GREAT, URL_ULTRA, URL_MASTER
except ImportError:
    URL_GREAT = "https://pvpoke.com/data/groups/lg/rankings_1500.json"
    URL_ULTRA = "https://pvpoke.com/data/groups/lg/rankings_2500.json"
    URL_MASTER = "https://pvpoke.com/data/groups/lg/rankings_10000.json"

# URL do código fonte do PvPoke para pegar o CPM
URL_JS_PVPOKE = "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/js/pokemon/Pokemon.js"
# URL para os Base Stats (Gamemaster)
URL_GAMEMASTER = "https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster.json"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

def update_json(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        path = os.path.join(DATA_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4)
        print(f"✅ {filename} atualizado.")
    except Exception as e:
        print(f"❌ Erro ao atualizar {filename}: {e}")

def update_cpm_from_js():
    try:
        print("🔍 Buscando CPM no código do PvPoke...")
        response = requests.get(URL_JS_PVPOKE)
        content = response.text
        
        # Regex para capturar o array 'var cpms = [...];'
        match = re.search(r'var cpms = \[(.*?)\];', content, re.DOTALL)
        if match:
            raw_array = match.group(1).strip()
            # Limpa e converte para lista de floats
            cpm_list = [float(x.strip()) for x in raw_array.split(',') if x.strip()]
            
            path = os.path.join(DATA_DIR, "cpm.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"cpms": cpm_list}, f, indent=4)
            print(f"✅ cpm.json gerado com {len(cpm_list)} valores.")
    except Exception as e:
        print(f"❌ Erro ao extrair CPM: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando atualização de dados...")
    update_json(URL_GREAT, "base_great.json")
    update_json(URL_ULTRA, "base_ultra.json")
    update_json(URL_MASTER, "base_master.json")
    update_json(URL_GAMEMASTER, "gamemaster.json")
    update_cpm_from_js()
    print("✨ Processo concluído.")