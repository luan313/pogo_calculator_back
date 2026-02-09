from ..utils.catchers.league_catcher import find_league_rank
from ..utils.catchers.iv_catcher import find_iv_rank_great, find_iv_rank_ultra, find_iv_rank_master

from ..api.models import DataToStoreModel

def great_fetcher(data: dict, output: DataToStoreModel):
    output.rank_liga_grande = find_league_rank(data, output.nome)

    if output.rank_liga_grande:
        output.rank_iv_grande = find_iv_rank_great(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)

def ultra_fetcher(data: dict, output: DataToStoreModel):
    output.rank_liga_ultra = find_league_rank(data, output.nome)

    if output.rank_liga_ultra:
        output.rank_iv_ultra = find_iv_rank_ultra(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)

def master_fetcher(data: dict, output: DataToStoreModel):
    output.rank_liga_mestra = find_league_rank(data, output.nome)

    if output.rank_liga_mestra:
        output.rank_iv_mestra = find_iv_rank_master(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)