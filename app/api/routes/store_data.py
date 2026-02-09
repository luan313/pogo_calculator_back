from fastapi import APIRouter, HTTPException
from ..models import DataToStoreModel, PokemonInput, ResponseStatus
from ...services.rank_fetcher import great_fetcher, ultra_fetcher, master_fetcher
from ...utils.supabase_utils.insert import insert_pokemon
from ...utils.base_loader import carregar_base

router = APIRouter()

@router.post("/store_data", response_model=ResponseStatus)
def store_data(payload: PokemonInput):
    name = payload.nome

    contador = 0

    base_great = carregar_base('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_great.json')
    base_ultra = carregar_base('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_ultra.json')
    base_master = carregar_base('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_master.json')
    
    for each in payload.ivs:
        output = DataToStoreModel(
            nome=name,
            ataque_iv = each.ataque_iv,
            defesa_iv = each.defesa_iv,
            hp_iv = each.hp_iv
        )
        

        output.rank_liga_grande = None
        output.rank_iv_grande = None
        great_fetcher(base_great, output)

        output.rank_liga_ultra = None
        output.rank_iv_ultra = None
        ultra_fetcher(base_ultra, output)

        output.rank_liga_mestra = None
        output.rank_iv_mestra = None
        master_fetcher(base_master, output)
    
        insert_pokemon(output)
        contador += 1

    return ResponseStatus(
        status="SUCCESS",
        message=f"Foram adicionados {contador} Pokémon."
    )