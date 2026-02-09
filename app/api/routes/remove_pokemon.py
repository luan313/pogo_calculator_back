from fastapi import APIRouter, HTTPException

from ...utils.supabase_utils.delete import delete_pokemon

router = APIRouter()

@router.delete("/remove_pokemon")
def remove_pokemon(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    try:
        delete_pokemon(name, atk_iv, def_iv, hp_iv)

        return {
            "status": "SUCCESS",
            "message": "Pokémon removido."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar {str(e)}")