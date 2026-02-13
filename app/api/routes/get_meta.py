import logging
from fastapi import APIRouter
from app.utils.safe_load import safe_load
from app.services.dex_fetcher import dex_fetcher
from app.config import URL_GREAT, URL_ULTRA, URL_MASTER, URL_GAMEMASTER, TYPES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

SPECIAL_TAGS = {"legendary", "mythical", "ultrabeast", "mega", "wildlegendary"}

BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)
GAMEMASTER_DATA = safe_load("gamemaster.json", URL_GAMEMASTER) 

def build_metadata_map(gamemaster):
    """Constrói um mapa contendo Nome, Tipos e Tags para acesso O(1)."""
    meta_map = {}
    if not gamemaster:
        logger.error("Gamemaster vazio ou não carregado!")
        return meta_map
    
    data_list = gamemaster.get('pokemon', []) if isinstance(gamemaster, dict) else gamemaster
    
    for p in data_list:
        s_id = p.get('speciesId', '')
        if s_id:
            # --- MUDANÇA AQUI: Tratamento do nome (Shadow) -> Sombroso ---
            raw_name = p.get('speciesName', s_id)
            # Substitui "(Shadow)" por "Sombroso", removendo os parênteses
            final_name = raw_name.replace("(Shadow)", "Sombroso")
            
            meta_map[s_id] = {
                "name": final_name, 
                "types": p.get('types', []),
                "tags": set(p.get('tags', [])) 
            }
            
    logger.info(f"Mapa de metadados construído com {len(meta_map)} Pokémons.")
    return meta_map

# Executa a construção do mapa
METADATA_LOOKUP = build_metadata_map(GAMEMASTER_DATA)

def filter_top_six_by_type(base_data, poke_type, include_specials):
    if not base_data:
        return []

    top_six = []
    
    for rank, poke in enumerate(base_data, start=1):
        species_id = poke.get("speciesId")
        
        poke_data = METADATA_LOOKUP.get(species_id)
        
        if not poke_data:
            continue 

        poke_types = poke_data["types"]
        poke_tags = poke_data["tags"]
        poke_name = poke_data["name"]

        is_special = not poke_tags.isdisjoint(SPECIAL_TAGS)

        if not include_specials and is_special:
            continue

        if poke_type in poke_types:
            top_six.append({
                "nome": poke_name,
                "tipo": poke_types,
                "rank_liga": rank
            })
            
        if len(top_six) == 6:
            break
            
    return top_six

@router.get("/get_meta")
def get_meta(include_specials: bool = False):
    logger.info(f"Iniciando /get_meta. Incluir especiais: {include_specials}")
    
    if not METADATA_LOOKUP:
        return {"error": "Dados de tipagem (Gamemaster) não carregados."}

    meta_final = {"great": {}, "ultra": {}, "master": {}}
    leagues = {"great": BASE_GREAT, "ultra": BASE_ULTRA, "master": BASE_MASTER}

    try:
        for league_name, base_data in leagues.items():
            if not base_data:
                continue

            for t in TYPES:
                meta_final[league_name][t] = filter_top_six_by_type(base_data, t, include_specials)

        dex_fetcher(meta_final)

        return meta_final

    except Exception as e:
        logger.error(f"Erro crítico em get_meta: {str(e)}", exc_info=True)
        return {"error": str(e)}