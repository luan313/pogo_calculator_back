from typing import List

def dex_catcher(dex_map: dict, tier_list: dict, league: str):
    for categorie_name, pokemon_list in tier_list[league].items():
        if not isinstance(pokemon_list, list):
            continue

        for pokemon in pokemon_list:
            name_id = pokemon["nome"].lower().replace(" ", "_")

            pokemon["dex"] = dex_map.get(name_id, 0)