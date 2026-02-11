from fastapi import APIRouter, HTTPException, Depends
from ..models import DataToStoreModel, PokemonInput, ResponseStatus
import logging

from ...services.rank_fetcher import great_fetcher, ultra_fetcher, master_fetcher
from ...utils.supabase_utils.insert import insert_pokemon
from ..auth_dependency import get_current_user
from app.utils.safe_load import safe_load
from ...config import URL_GREAT, URL_ULTRA, URL_MASTER

logger = logging.getLogger(__name__)

# Carregamento robusto
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)

router = APIRouter()

@router.post("/store_data", response_model=ResponseStatus)
def store_data(
    payload: PokemonInput,
    user = Depends(get_current_user)
):
    try:
        current_user_id = user.id
        name = payload.nome
        typep = payload.tipo
        contador = 0

        if not name or not typep:
            raise HTTPException(status_code=400, detail="Nome e tipo são obrigatórios.")
        
        for each in payload.ivs:
            output = DataToStoreModel(
                user_id=current_user_id,
                nome=name,
                tipo=typep,
                ataque_iv = each.ataque_iv,
                defesa_iv = each.defesa_iv,
                hp_iv = each.hp_iv
            )
            
            great_fetcher(BASE_GREAT, output)
            ultra_fetcher(BASE_ULTRA, output)
            master_fetcher(BASE_MASTER, output)
        
            insert_pokemon(output)
            contador += 1

        return ResponseStatus(
            status="SUCCESS",
            message=f"Foram adicionados {contador} Pokémon."
        )

    except Exception as e:
        logger.error(f"Erro ao salvar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")