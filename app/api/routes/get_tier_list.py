from fastapi import APIRouter, Depends
import logging

from ..auth_dependency import get_current_user

from ...utils.supabase_utils.type_tier_list import get_pokemon_by_tier

from app.config import TYPES

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get_tier_list")
def get_tier_list(user = Depends(get_current_user)):
    user_id = user.id

    tier_list = {
        "great": {},
        "ultra": {},
        "master": {}
    }

    try:
        for t in TYPES:
            tier_list["great"][t] = get_pokemon_by_tier("rank_liga_grande", "rank_iv_grande", t, user_id)
            tier_list["ultra"][t] = get_pokemon_by_tier("rank_liga_ultra", "rank_iv_ultra", t, user_id)
            tier_list["master"][t] = get_pokemon_by_tier("rank_liga_mestra", "rank_iv_mestra", t, user_id)

        return tier_list

    except Exception as e:
        logger.error(f"Erro ao buscar tier list para o usuário {user_id}: {e}")
        return {"error": "Falha ao carregar seus dados."}