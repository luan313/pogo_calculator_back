from fastapi import APIRouter, Depends
import logging

from ..auth_dependency import get_current_user

from ...utils.supabase_utils.type_tier_list import get_great_pokemon, get_ultra_pokemon, get_master_pokemon

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
        for typep in TYPES:
            tier_list["great"][typep] = get_great_pokemon(typep, user_id)
            tier_list["ultra"][typep] = get_ultra_pokemon(typep, user_id)
            tier_list["master"][typep] = get_master_pokemon(typep, user_id)

        return tier_list

    except Exception as e:
        logger.error(f"Erro ao buscar tier list para o usuário {user_id}: {e}")
        return {"error": "Falha ao carregar seus dados."}