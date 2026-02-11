import logging
from fastapi import APIRouter
from app.utils.safe_load import safe_load
from app.services.dex_fetcher import dex_fetcher
from app.config import URL_GREAT, URL_ULTRA, URL_MASTER, URL_GAMEMASTER, TYPES

# Configuração básica do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Tags que definem um Pokémon como "Especial" (removidos se include_specials=False)
SPECIAL_TAGS = {"legendary", "mythical", "ultrabeast", "mega", "wildlegendary"}

# 1. Carrega as Bases
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)
GAMEMASTER_DATA = safe_load("gamemaster.json", URL_GAMEMASTER) 

# 2. Mapa de Metadados (Tipos E Tags)
def build_metadata_map(gamemaster):
    """Constrói um mapa contendo Tipos e Tags para acesso O(1)."""
    meta_map = {}
    if not gamemaster:
        logger.error("Gamemaster vazio ou não carregado!")
        return meta_map
    
    data_list = gamemaster.get('pokemon', []) if isinstance(gamemaster, dict) else gamemaster
    
    for p in data_list:
        s_id = p.get('speciesId', '')
        if s_id:
            # Agora guardamos um objeto com tipos E tags
            meta_map[s_id] = {
                "types": p.get('types', []),
                "tags": set(p.get('tags', [])) # Set para busca rápida
            }
            
    logger.info(f"Mapa de metadados construído com {len(meta_map)} Pokémons.")
    return meta_map

# Executa a construção do mapa (agora chamado de METADATA_LOOKUP)
METADATA_LOOKUP = build_metadata_map(GAMEMASTER_DATA)

def filter_top_six_by_type(base_data, poke_type, include_specials):
    """
    Retorna os 6 melhores por tipo.
    Se include_specials for False, ignora lendários/míticos.
    """
    if not base_data:
        return []

    top_six = []
    
    for rank, poke in enumerate(base_data, start=1):
        species_id = poke.get("speciesId")
        
        # Busca os dados no mapa auxiliar
        poke_data = METADATA_LOOKUP.get(species_id)
        
        if not poke_data:
            continue # Se não achou no gamemaster, pula por segurança

        poke_types = poke_data["types"]
        poke_tags = poke_data["tags"]

        # --- LÓGICA DE FILTRO DE ESPECIAIS ---
        # Verifica se o pokemon tem alguma tag que está na lista de SPECIAL_TAGS
        is_special = not poke_tags.isdisjoint(SPECIAL_TAGS)

        # Se o usuário NÃO quer especiais, e o bicho É especial -> Pula (continue)
        if not include_specials and is_special:
            continue
        # -------------------------------------

        if poke_type in poke_types:
            top_six.append({
                "nome": species_id,
                "tipo": poke_types,
                "rank_liga": rank
            })
            
        if len(top_six) == 6:
            break
            
    return top_six

@router.get("/get_meta")
def get_meta(include_specials: bool = False): # Default False se não enviado
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
                # Agora passamos o boolean 'include_specials' para a função de filtro
                meta_final[league_name][t] = filter_top_six_by_type(base_data, t, include_specials)

        dex_fetcher(meta_final)

        return meta_final

    except Exception as e:
        logger.error(f"Erro crítico em get_meta: {str(e)}", exc_info=True)
        return {"error": str(e)}