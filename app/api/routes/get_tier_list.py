from fastapi import APIRouter

from ...utils.supabase_utils.type_tier_list import get_great_pokemon, get_ultra_pokemon, get_master_pokemon

from app.config import TYPES

router = APIRouter()

@router.get("/get_tier_list")
def get_tier_list():
    tier_list = {
        "great": {},
        "ultra": {},
        "master": {}
    }

    try:
        for typep in TYPES:
            tier_list["great"][typep] = get_great_pokemon(typep)
            tier_list["ultra"][typep] = get_ultra_pokemon(typep)
            tier_list["master"][typep] = get_master_pokemon(typep)

        return tier_list

    except Exception as e:
        print(f"Erro ao gerar tier list: {e}")
        return {"error": "Falha ao processar dados", "details": str(e)}