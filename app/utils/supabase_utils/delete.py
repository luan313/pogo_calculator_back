from .connect import SupabaseConnection

def delete_pokemon(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    response = (
        SupabaseConnection.table("pokemons")
        .delete()
        .eq("name", name, "ataque_iv", atk_iv, "defesa_iv", def_iv, "hp_iv", hp_iv)
        .execute()
    )