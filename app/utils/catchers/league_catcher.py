def find_league_rank(base_dados, name: str):
    for rank, pokemon in enumerate(base_dados, start=1):
        if pokemon.get("speciesId") == name.lower():
            return rank
    return None