from fastapi import APIRouter, Query
from typing import List, Dict
import requests
from ..models import PokemonSuggestion

router = APIRouter()

gm_data = requests.get("https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster.json").json()

POKEMON_MAP = {p["speciesId"]: p["types"] for p in gm_data["pokemon"]}
POKEMON_IDS = List(POKEMON_MAP.keys())

@router.get("/autocomplete", response_model=List[PokemonSuggestion])
def autocomplete(q: str = Query(..., min_length=1)):
    query = q.lower()
    
    sugestoes = [name for name in POKEMON_IDS if name.lower().startswith(query)]
    
    if len(sugestoes) < 5:
        contem = [name for name in POKEMON_IDS if query in name.lower() and name not in sugestoes]
        sugestoes.extend(contem)

    resultado = [
        PokemonSuggestion(name=name, types=POKEMON_MAP[name])
        for name in sugestoes[:10]
    ]

    return resultado