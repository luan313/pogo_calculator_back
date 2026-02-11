import logging
from fastapi import APIRouter
from app.utils.safe_load import safe_load
from app.services.dex_fetcher import dex_fetcher
from app.config import URL_GREAT, URL_ULTRA, URL_MASTER, URL_GAMEMASTER, TYPES

# Configuração básica do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 1. Carrega as Bases de Ranking (Ranking PvPoke)
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)

# 2. Carrega o GameMaster (Dados brutos com tipagem)
# Obs: Se não tiver URL pública do gamemaster, passe None ou uma URL válida.
GAMEMASTER_DATA = safe_load("gamemaster.json", URL_GAMEMASTER) 

# 3. Criação do Mapa de Tipos (Hash Map para busca rápida)
# Transforma a lista do gamemaster em um dicionário: { "pikachu": ["electric"], ... }
def build_type_map(gamemaster):
    type_map = {}
    if not gamemaster:
        logger.error("Gamemaster vazio ou não carregado!")
        return type_map
    
    # Verifica se o gamemaster é uma lista ou um dict com chave 'pokemon'
    data_list = gamemaster.get('pokemon', []) if isinstance(gamemaster, dict) else gamemaster
    
    for p in data_list:
        # Normaliza o ID para garantir compatibilidade (ex: "Charizard" -> "charizard")
        s_id = p.get('speciesId', '')
        if s_id:
            type_map[s_id] = p.get('types', [])
            
    logger.info(f"Mapa de tipos construído com {len(type_map)} Pokémons.")
    return type_map

# Executa a construção do mapa ao iniciar
TYPE_LOOKUP = build_type_map(GAMEMASTER_DATA)

def filter_top_six_by_type(base_data, poke_type):
    """Retorna apenas os 6 melhores por tipo, consultando o TYPE_LOOKUP."""
    if not base_data:
        return []

    top_six = []
    
    # Itera sobre o ranking
    for rank, poke in enumerate(base_data, start=1):
        species_id = poke.get("speciesId")
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # Em vez de ler do poke (que não tem tipo), buscamos no mapa auxiliar
        poke_types = TYPE_LOOKUP.get(species_id, []) 
        
        if poke_type in poke_types:
            top_six.append({
                "nome": species_id,
                "tipo": poke_types, # Retorna a tipagem completa encontrada no Gamemaster
                "rank_liga": rank
            })
            
        if len(top_six) == 6:
            break
            
    return top_six

@router.get("/get_meta")
def get_meta():
    logger.info("Iniciando processamento da rota /get_meta")
    
    # Debug rápido para ver se o mapa está funcionando
    if not TYPE_LOOKUP:
        logger.critical("ERRO CRÍTICO: TYPE_LOOKUP está vazio. Verifique o arquivo gamemaster.json")
        return {"error": "Dados de tipagem (Gamemaster) não carregados."}

    meta_final = {"great": {}, "ultra": {}, "master": {}}
    leagues = {"great": BASE_GREAT, "ultra": BASE_ULTRA, "master": BASE_MASTER}

    try:
        for league_name, base_data in leagues.items():
            if not base_data:
                continue

            for t in TYPES:
                meta_final[league_name][t] = filter_top_six_by_type(base_data, t)

        # Injeta o número da dex para as imagens
        dex_fetcher(meta_final)

        return meta_final

    except Exception as e:
        logger.error(f"Erro crítico em get_meta: {str(e)}", exc_info=True)
        return {"error": str(e)}