from fastapi import APIRouter, HTTPException
from ..models import DataToStoreModel, PokemonInput, ResponseStatus
from ...services.rank_fetcher import great_fetcher, ultra_fetcher, master_fetcher
from ...utils.supabase_utils.insert import insert_pokemon
from ...utils.base_loader import carregar_base
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_great = os.path.join(BASE_DIR, "data", "base_great.json")
BASE_GREAT = carregar_base(path_great)

path_ultra = os.path.join(BASE_DIR, "data", "base_ultra.json")
BASE_ULTRA = carregar_base(path_ultra)

path_master = os.path.join(BASE_DIR, "data", "base_master.json")
BASE_MASTER = carregar_base(path_master)

router = APIRouter()

@router.post("/store_data", response_model=ResponseStatus)
def store_data(payload: PokemonInput):
    name = payload.nome
    typep = payload.tipo

    contador = 0

    
    for each in payload.ivs:
        output = DataToStoreModel(
            nome=name,
            tipo=typep,
            ataque_iv = each.ataque_iv,
            defesa_iv = each.defesa_iv,
            hp_iv = each.hp_iv
        )
        

        output.rank_liga_grande = None
        output.rank_iv_grande = None
        great_fetcher(BASE_GREAT, output)

        output.rank_liga_ultra = None
        output.rank_iv_ultra = None
        ultra_fetcher(BASE_ULTRA, output)

        output.rank_liga_mestra = None
        output.rank_iv_mestra = None
        master_fetcher(BASE_MASTER, output)
    
        insert_pokemon(output)
        contador += 1

    return ResponseStatus(
        status="SUCCESS",
        message=f"Foram adicionados {contador} Pokémon."
    )