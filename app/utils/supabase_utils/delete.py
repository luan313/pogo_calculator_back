from .connect import SupabaseConnection

def delete_pokemon(name: str, atk_iv: int, def_iv: int, hp_iv: int, user_id: str):
    response = (
        SupabaseConnection.table("pokemons")
        .delete()
        .eq("nome", name)
        .eq("ataque_iv", atk_iv)
        .eq("defesa_iv", def_iv)
        .eq("hp_iv", hp_iv)
        .eq("user_id", user_id) # O FILTRO DE SEGURANÇA
        .execute()
    )
    return response