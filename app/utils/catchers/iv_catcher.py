import logging
from ..pogo_iv_rank import get_rank

# Configura o logger para este arquivo específico
logger = logging.getLogger(__name__)

def find_iv_rank_great(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    logger.info(f"📊 [GREAT] Chamando get_rank para {name} ({atk_iv}/{def_iv}/{hp_iv})")
    try:
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=1500)
        logger.info(f"✅ [GREAT] Resultado recebido: {result}")
        return result
    except Exception as e:
        # Aqui capturamos o erro real em vez de apenas retornar None
        logger.error(f"❌ [GREAT] Falha crítica ao obter rank para {name}: {str(e)}")
        return None

def find_iv_rank_ultra(name, atk_iv, def_iv, hp_iv):
    logger.info(f"📊 [ULTRA] Chamando get_rank para {name}")
    try:
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=2500)
        logger.info(f"✅ [ULTRA] Resultado recebido: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [ULTRA] Falha crítica para {name}: {str(e)}")
        return None

def find_iv_rank_master(name, atk_iv, def_iv, hp_iv):
    logger.info(f"📊 [MASTER] Chamando get_rank para {name}")
    try:
        # Note que para Master o league costuma ser 0 ou 10000 dependendo do site
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=0)
        logger.info(f"✅ [MASTER] Resultado recebido: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [MASTER] Falha crítica para {name}: {str(e)}")
        return None