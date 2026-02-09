import logging
from ..utils.catchers.league_catcher import find_league_rank
from ..utils.catchers.iv_catcher import find_iv_rank_great, find_iv_rank_ultra, find_iv_rank_master

from ..api.models import DataToStoreModel

logger = logging.getLogger(__name__)

def great_fetcher(data: dict, output: DataToStoreModel):
    logger.info(f"Iniciando busca Great League para: {output.nome}")
    
    if not data:
        logger.error("A base de dados da Great League não foi carregada corretamente.")
        return

    output.rank_liga_grande = find_league_rank(data, output.nome)
    logger.debug(f"Resultado find_league_rank (Great): {output.rank_liga_grande}")

    if not data:
        logger.error("A base de dados da Ultra League não foi carregada corretamente.")
        return

    if output.rank_liga_grande:
        logger.info(f"Rank {output.rank_liga_grande} encontrado. Calculando IV Rank...")
        output.rank_iv_grande = find_iv_rank_great(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)
        logger.info(f"IV Rank calculado: {output.rank_iv_grande}")

    else:
        logger.warning(f"Pokémon '{output.nome}' não encontrado nos dados da Great League.")

def ultra_fetcher(data: dict, output: DataToStoreModel):
    logger.info(f"Iniciando busca Ultra League para: {output.nome}")
    output.rank_liga_ultra = find_league_rank(data, output.nome)

    if not data:
        logger.error("A base de dados da Master League não foi carregada corretamente.")
        return

    if output.rank_liga_ultra:
        logger.info(f"Rank {output.rank_liga_ultra} encontrado em Ultra. Calculando IV...")
        output.rank_iv_ultra = find_iv_rank_ultra(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)
        logger.info(f"IV Rank calculado: {output.rank_iv_ultra}")

    else:
        logger.warning(f"Pokémon '{output.nome}' não encontrado nos dados da Ultra League.")

def master_fetcher(data: dict, output: DataToStoreModel):
    logger.info(f"Iniciando busca Master League para: {output.nome}")
    output.rank_liga_mestra = find_league_rank(data, output.nome)

    if output.rank_liga_mestra:
        logger.info(f"Rank {output.rank_liga_mestra} encontrado em Master. Calculando IV...")
        output.rank_iv_mestra = find_iv_rank_master(output.nome, output.ataque_iv, output.defesa_iv, output.hp_iv)
        logger.info(f"IV Rank calculado: {output.rank_iv_mestra}")


    else:
        logger.warning(f"Pokémon '{output.nome}' não encontrado nos dados da Master League.")   