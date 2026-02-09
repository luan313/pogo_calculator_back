from fastapi import APIRouter

from ...utils.supabase_utils.type_tier_list import get_great_pokemon, get_ultra_pokemon, get_master_pokemon

from ....config import TYPES

router = APIRouter()

@router.get("/get_tier_list")
def get_tier_list():
    tier_list = {}

    for typep in TYPES:
        tier_list["great"][typep] = get_great_pokemon
        tier_list["ultra"][typep] = get_ultra_pokemon
        tier_list["master"][typep] = get_master_pokemon

    return tier_list