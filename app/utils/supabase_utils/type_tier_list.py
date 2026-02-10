from .connect import SupabaseConnection

def get_great_pokemon(typep: str, user_id: str):
    response = (
        SupabaseConnection.table("great_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .eq("user_id", user_id)
        .execute()
    )

    return response.data

def get_ultra_pokemon(typep: str, user_id: str):
    response = (
        SupabaseConnection.table("ultra_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .eq("user_id", user_id)
        .execute()
    )

    return response.data

def get_master_pokemon(typep: str, user_id: str):
    response = (
        SupabaseConnection.table("master_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .eq("user_id", user_id)
        .execute()
    )

    return response.data