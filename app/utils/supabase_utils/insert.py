from .connect import SupabaseConnection
from ...api.models import DataToStoreModel

def insert_pokemon(data: DataToStoreModel):
    response = (
        SupabaseConnection.table("pokemons")
        .insert({
            "nome": data.nome,
            "tipo": data.tipo,
            "ataque_iv": data.ataque_iv,
            "defesa_iv": data.defesa_iv,
            "hp_iv": data.hp_iv,
            "rank_iv_grande": data.rank_iv_grande,          
            "rank_iv_ultra": data.rank_iv_ultra,          
            "rank_iv_mestra": data.rank_iv_mestra,          
            "rank_liga_grande": data.rank_liga_grande,          
            "rank_liga_ultra": data.rank_liga_ultra,           
            "rank_liga_mestra": data.rank_liga_mestra,          
        })
    )

    return response