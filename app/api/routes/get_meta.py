import logging
from fastapi import APIRouter
from app.utils.safe_load import safe_load
from app.services.dex_fetcher import dex_fetcher
from app.config import URL_GREAT, URL_ULTRA, URL_MASTER, TYPES

logger = logging.getLogger(__name__)

router = APIRouter()

# Bases carregadas e ordenadas pelo Rank do PvPoke
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)

def filter_top_six_by_type(base_data, poke_type):
    """Retorna apenas os 6 melhores por tipo elemental."""
    # Log para verificar se a base de dados chegou aqui
    if not base_data:
        logger.warning(f"filter_top_six_by_type recebeu base_data vazia ou Nula para o tipo {poke_type}")
        return []

    top_six = []
    for rank, poke in enumerate(base_data, start=1):
        # Log de debug profundo (cuidado em produção, pode gerar muito texto)
        # logger.debug(f"Verificando {poke.get('speciesId')} - Tipos: {poke.get('types')}")
        
        if poke_type in poke.get("types", []):
            top_six.append({
                "nome": poke.get("speciesId"), 
                "tipo": poke.get("types"),
                "rank_liga": rank
            })
        if len(top_six) == 6:
            break
            
    return top_six

@router.get("/get_meta")
def get_meta():
    logger.info("Iniciando processamento da rota /get_meta")
    
    meta_final = {"great": {}, "ultra": {}, "master": {}}
    
    # Verifica se as bases globais foram carregadas
    logger.info(f"Status das Bases - Great: {len(BASE_GREAT) if BASE_GREAT else 'None'}, "
                f"Ultra: {len(BASE_ULTRA) if BASE_ULTRA else 'None'}, "
                f"Master: {len(BASE_MASTER) if BASE_MASTER else 'None'}")

    leagues = {"great": BASE_GREAT, "ultra": BASE_ULTRA, "master": BASE_MASTER}

    try:
        for league_name, base_data in leagues.items():
            logger.info(f"Processando liga: {league_name}")
            
            if not base_data:
                logger.error(f"Base de dados vazia para a liga {league_name}. Pulando.")
                continue

            # Itera apenas sobre os tipos elementais definidos no config
            for t in TYPES:
                filtered_list = filter_top_six_by_type(base_data, t)
                meta_final[league_name][t] = filtered_list
                
                # Log se não encontrar nenhum pokemon para um tipo específico (pode indicar erro no nome do tipo em TYPES ou no JSON)
                if not filtered_list:
                    logger.warning(f"Nenhum pokemon encontrado para Liga: {league_name} | Tipo: {t}")

        # Injeta o número da dex para as imagens (pm{dex}.icon.png)
        logger.info("Iniciando dex_fetcher...")
        dex_fetcher(meta_final)
        logger.info("dex_fetcher finalizado com sucesso.")

        return meta_final

    except Exception as e:
        # exc_info=True garante que o traceback completo apareça no terminal
        logger.error(f"Erro crítico em get_meta: {str(e)}", exc_info=True)
        return {"error": str(e)}