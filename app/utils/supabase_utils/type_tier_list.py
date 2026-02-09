from .connect import SupabaseConnection

def get_great_pokemon(typep: str):
    response = (
        SupabaseConnection.table("great_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .execute()
    )

    return response

def get_ultra_pokemon(typep: str):
    response = (
        SupabaseConnection.table("ultra_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .execute()
    )

    return response

def get_master_pokemon(typep: str):
    response = (
        SupabaseConnection.table("master_pokemon_by_type")
        .select("*")
        .eq("tipo", typep)
        .execute()
    )

    return response