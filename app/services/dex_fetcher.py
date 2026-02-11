import logging
import os

from app.utils.catchers.dex_catcher import dex_catcher
from app.api.routes.store_data import safe_load
from app.config import URL_GAMEMASTER

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carregamento robusto
BASE_GAMEMASTER = safe_load("gamemaster.json", URL_GAMEMASTER)

def dex_fetcher(tier_list: dict):
    pokemon_data = BASE_GAMEMASTER.get("pokemon")
    dex_map = {p["speciesId"]: p["dex"] for p in pokemon_data if "speciesId" in p and "dex" in p}

    for league in ["great", "ultra", "master"]:
        dex_catcher(dex_map, tier_list, league)