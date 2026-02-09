from fastapi import APIRouter, Query
from typing import List
import requests

router = APIRouter()

data = requests.get("https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster.json").json()
POKEMON_IDS = [p["speciesId"] for p in data["pokemon"]]

@router.get("/autocomplete", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1)):
    query = q.lower()
    
    sugestoes = [name for name in POKEMON_IDS if name.lower().startswith(query)]
    
    if len(sugestoes) < 5:
        contem = [name for name in POKEMON_IDS if query in name.lower() and name not in sugestoes]
        sugestoes.extend(contem)

    return sugestoes[:10]