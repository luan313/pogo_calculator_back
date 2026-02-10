import requests
import json
import os
import re

from app.utils.supabase_utils.connect import SupabaseConnection

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

def sanitize_name(name):
    """
    Transforma 'Sirfetch'd Shadow' em 'sirfetchd_shadow'
    para bater exatamente com o speciesId do PvPoke.
    """
    if not name: return ""
    # 1. Tudo para minúsculo
    name = name.lower()
    # 2. Remove apóstrofos e pontos (Sirfetch'd -> sirfetchd / Mr. Mime -> mr mime)
    name = name.replace("'", "").replace(".", "")
    # 3. Substitui espaços por underscores (blastoise shadow -> blastoise_shadow)
    name = name.replace(" ", "_")
    # 4. Remove qualquer caractere que não seja letra, número ou underscore
    return re.sub(r'[^a-z0-9_]', '', name)

def load_rankings_as_map(filename):
    """
    Equivalente à sua função find_league_rank, mas mapeia TODOS de uma vez.
    """
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # O índice (i) + 1 é o Rank. Criamos o mapa { "speciesId": Rank }
        return {p.get("speciesId"): i for i, p in enumerate(data, start=1)}

def sync_database_ranks():
    # 1. Carrega os mapas de rank (Aqui o enumerate acontece uma vez por liga)
    ranks_great = load_rankings_as_map("base_great.json")
    ranks_ultra = load_rankings_as_map("base_ultra.json")
    ranks_master = load_rankings_as_map("base_master.json")

    try:
        response = SupabaseConnection.table("pokemons").select("nome").execute()
        unique_names = list(set([p['nome'] for p in response.data]))

        for name in unique_names:
            # 2. Limpa o nome para o formato speciesId do PvPoke
            sid = sanitize_name(name)
            
            # 3. Busca o rank no mapa (O(1) - Instantâneo)
            # Se não achar (None), o banco de dados guardará NULL
            val_great = ranks_great.get(sid)
            val_ultra = ranks_ultra.get(sid)
            val_master = ranks_master.get(sid)

            # 4. Update no Supabase
            SupabaseConnection.table("pokemons").update({
                "rank_liga_grande": val_great,
                "rank_liga_ultra": val_ultra,
                "rank_liga_mestra": val_master
            }).eq("nome", name).execute()
            
            print(f"✅ {name} sincronizado (ID: {sid})")

    except Exception as e:
        print(f"❌ Erro: {e}")

# No seu bloco principal, basta adicionar a chamada:
if __name__ == "__main__":
    print("🚀 Iniciando atualização de dados...")
    update_json(URL_GREAT, "base_great.json")
    update_json(URL_ULTRA, "base_ultra.json")
    update_json(URL_MASTER, "base_master.json")
    update_json(URL_GAMEMASTER, "gamemaster.json")
    update_cpm_from_js()
    
    # Nova etapa de sincronização
    sync_database_ranks()
    
    print("✨ Processo concluído.")