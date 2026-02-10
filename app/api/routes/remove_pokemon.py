from fastapi import APIRouter, HTTPException, Depends
from ..auth_dependency import get_current_user # Sua dependência de login
from ...utils.supabase_utils.delete import delete_pokemon

router = APIRouter()

@router.delete("/remove_pokemon")
def remove_pokemon(
    name: str, 
    atk_iv: int, 
    def_iv: int, 
    hp_iv: int,
    user = Depends(get_current_user) # Injeção do usuário logado
):
    try:
        # Passamos o ID do usuário para garantir a "posse" do registro
        user_id = user.id
        
        result = delete_pokemon(name, atk_iv, def_iv, hp_iv, user_id)

        # Verificamos se algo foi realmente deletado
        if not result.data:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado ou você não tem permissão.")

        return {
            "status": "SUCCESS",
            "message": f"Pokémon {name} removido com sucesso."
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")