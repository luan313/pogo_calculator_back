import logging
from ..pogo_iv_rank import get_rank

# Configura o logger para este arquivo específico
logger = logging.getLogger(__name__)

def sanitize_name(name: str) -> str:
    """Ajusta o nome para o formato do gamemaster (ex: 'Mr. Mime' -> 'mr_mime')"""
    return name.lower().replace(" ", "_").replace(".", "").replace("'", "")

def find_iv_rank_great(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    # Higieniza o nome antes de enviar
    pokemon_id = sanitize_name(name)
    logger.info(f"📊 [GREAT] Calculando rank para {pokemon_id} ({atk_iv}/{def_iv}/{hp_iv})")
    
    try:
        # A nova get_rank matemática agora processa isso localmente
        result = get_rank(pokemon_id, atk_iv, def_iv, hp_iv, league=1500)
        logger.info(f"✅ [GREAT] Resultado: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [GREAT] Erro no cálculo: {str(e)}")
        return None

def find_iv_rank_ultra(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    pokemon_id = sanitize_name(name)
    logger.info(f"📊 [ULTRA] Calculando rank para {pokemon_id}")
    
    try:
        result = get_rank(pokemon_id, atk_iv, def_iv, hp_iv, league=2500)
        logger.info(f"✅ [ULTRA] Resultado: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [ULTRA] Erro no cálculo: {str(e)}")
        return None

def find_iv_rank_master(name: str, atk_iv: int, def_iv: int, hp_iv: int):
    pokemon_id = sanitize_name(name)
    logger.info(f"📊 [MASTER] Calculando rank para {pokemon_id}")
    
    try:
        # Passar league=0 ativa a lógica de Master League na get_rank
        result = get_rank(pokemon_id, atk_iv, def_iv, hp_iv, league=0)
        logger.info(f"✅ [MASTER] Resultado: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [MASTER] Erro no cálculo: {str(e)}")
        return None