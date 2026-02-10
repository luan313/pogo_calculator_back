import json
import os
import logging
import math

logger = logging.getLogger(__name__)

# Caminho para os dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        logger.error(f"Arquivo {filename} não encontrado em {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_rank(pokemon_id: str, atk: int, df: int, hp: int, league: int):
    logger.info(f"📊 Calculando Rank IV (Matemático) para {pokemon_id} ({atk}/{df}/{hp}) na liga {league}")

    # 1. Carrega os dados necessários
    gm = load_json("gamemaster.json")
    cpm_data = load_json("cpm.json")

    if not gm or not cpm_data:
        return None

    cpms = cpm_data.get("cpms", [])
    
    # 2. Busca os Stats Base do Pokémon
    # No gamemaster do PvPoke, os pokémons ficam na chave "pokemon"
    pokemon_stats = next((p for p in gm.get("pokemon", []) if p.get("pokemonId") == pokemon_id.lower()), None)

    if not pokemon_stats:
        logger.warning(f"Pokémon {pokemon_id} não encontrado no gamemaster.")
        return None

    base_stats = pokemon_stats.get("baseStats")
    b_atk, b_def, b_hp = base_stats["atk"], base_stats["def"], base_stats["hp"]

    def get_stat_product(a, d, h, limit):
        best_sp = 0
        # Simula do nível 1 ao 50 (usando a tabela de CPM)
        for cpm in cpms:
            # Fórmula oficial de CP:
            # CP = floor((Atk * sqrt(Def) * sqrt(HP) * CPM^2) / 10)
            cur_atk = (b_atk + a) * cpm
            cur_def = (b_def + d) * cpm
            cur_hp = (b_hp + h) * cpm
            
            cp = math.floor((cur_atk * math.sqrt(cur_def) * math.sqrt(cur_hp)) / 10)
            
            # Se for Master League (limit 0 ou >= 10000), usamos nível 50 (último CPM)
            if limit <= 0 or limit >= 10000:
                # Master League costuma ser o último CPM disponível (Level 50)
                final_cpm = cpms[-1]
                return (b_atk + a) * (b_def + d) * (b_hp + h) * (final_cpm ** 3)

            if cp <= limit:
                best_sp = cur_atk * cur_def * math.floor(cur_hp) # Stat Product aproximado
            else:
                break
        return best_sp

    # 3. Calcula o Stat Product do usuário
    user_sp = get_stat_product(atk, df, hp, league)

    # 4. Gera todos os 4096 Stat Products possíveis para este Pokémon nesta liga
    all_products = []
    for i_a in range(16):
        for i_d in range(16):
            for i_h in range(16):
                all_products.append(get_stat_product(i_a, i_d, i_h, league))

    # 5. Ordena do maior para o menor e encontra a posição
    all_products.sort(reverse=True)
    
    try:
        # O Rank é o índice na lista ordenada + 1
        rank = all_products.index(user_sp) + 1
        logger.info(f"✅ Rank {rank} calculado localmente para {pokemon_id}")
        return rank
    except ValueError:
        logger.error("Erro ao localizar o produto de atributos na lista gerada.")
        return None