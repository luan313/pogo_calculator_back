from fastapi import APIRouter, Depends
from ..auth_dependency import get_current_user
from app.utils.safe_load import safe_load
from app.services.dex_fetcher import dex_fetcher
from app.config import URL_GREAT, URL_ULTRA, URL_MASTER, TYPES

router = APIRouter()

# Bases carregadas e ordenadas pelo Rank do PvPoke
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)

def filter_top_six_by_type(base_data, poke_type):
    """Retorna apenas os 6 melhores por tipo elemental."""
    top_six = []
    for rank, poke in enumerate(base_data, start=1):
        if poke_type in poke.get("types", []):
            top_six.append({
                "nome": poke.get("speciesId"), # Mantém speciesId para garantir as imagens
                "tipo": poke.get("types"),
                "rank_liga": rank
            })
        if len(top_six) == 6:
            break
    return top_six

@router.get("/get_meta")
def get_meta():
    meta_final = {"great": {}, "ultra": {}, "master": {}}
    leagues = {"great": BASE_GREAT, "ultra": BASE_ULTRA, "master": BASE_MASTER}

    try:
        for league_name, base_data in leagues.items():
            # Itera apenas sobre os tipos elementais definidos no config
            for t in TYPES:
                meta_final[league_name][t] = filter_top_six_by_type(base_data, t)

        # Injeta o número da dex para as imagens (pm{dex}.icon.png)
        dex_fetcher(meta_final)

        return meta_final

    except Exception as e:
        return {"error": str(e)}