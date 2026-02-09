from fastapi import APIRouter

from ...utils.supabase_utils.delete import delete_pokemon

router = APIRouter()

@router.delete("/remove_pokemon")
def remove_pokemon(name, atk_iv, def_iv, hp_iv):
    delete_pokemon(name, atk_iv, def_iv, hp_iv)