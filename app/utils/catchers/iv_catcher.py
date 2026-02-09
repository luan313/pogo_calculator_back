from ..pogo_iv_rank import get_rank

def find_iv_rank_great(name: str, atk_iv: int, def_iv: int, hp_iv:int):
    try:
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=1500)

        return result
    except:
        return None

def find_iv_rank_ultra(name, atk_iv, def_iv, hp_iv):
    try:
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=2500)

        return result
    except:
        return None

def find_iv_rank_master(name, atk_iv, def_iv, hp_iv):
    try:
        result = get_rank(name, atk_iv, def_iv, hp_iv, league=0)

        return result
    except:
        return None